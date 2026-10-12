import os
import secrets

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.ads_client import list_accounts, fetch_search_terms, fetch_existing_negative_keywords
from app.ai_review import review_rows
from app.negative_rules import find_candidates, filter_already_negative, is_exempt_row
from app.mutate import add_negative_keywords
from app.profiles.registry import get_profile

app = FastAPI(title="Google Ads Negatif Kelime Bulucu")
templates = Jinja2Templates(directory="app/templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

security = HTTPBasic()


def require_auth(credentials: HTTPBasicCredentials = Depends(security)):
    expected_password = os.environ.get("APP_PASSWORD")
    if not expected_password:
        raise HTTPException(500, "APP_PASSWORD ortam değişkeni ayarlanmamış")
    correct_password = secrets.compare_digest(credentials.password, expected_password)
    if not correct_password:
        raise HTTPException(
            status_code=401,
            detail="Hatalı parola",
            headers={"WWW-Authenticate": "Basic"},
        )
    return True


class AnalyzeRequest(BaseModel):
    customer_id: str
    date_range: str = "LAST_30_DAYS"
    start_date: str | None = None
    end_date: str | None = None


class NegativeTerm(BaseModel):
    campaign_id: str
    search_term: str


class ApplyNegativesRequest(BaseModel):
    customer_id: str
    terms: list[NegativeTerm]
    validate_only: bool = False


@app.get("/", response_class=HTMLResponse)
def index(request: Request, _auth: bool = Depends(require_auth)):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/api/accounts")
def api_accounts(_auth: bool = Depends(require_auth)):
    try:
        return {"accounts": list_accounts()}
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(500, str(exc)) from exc


@app.post("/api/analyze")
def api_analyze(body: AnalyzeRequest, _auth: bool = Depends(require_auth)):
    try:
        search_terms = fetch_search_terms(
            body.customer_id, body.date_range, body.start_date, body.end_date
        )
    except ValueError as exc:
        raise HTTPException(400, str(exc)) from exc
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(500, str(exc)) from exc

    profile = get_profile(body.customer_id)
    candidates = find_candidates(search_terms, profile=profile)

    try:
        existing_negatives = fetch_existing_negative_keywords(body.customer_id)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(500, str(exc)) from exc

    # Kurallardan geçen (negatif sayılmayan) satırları, zaten negatif olanlar
    # ve muaf kampanya/marka aramaları hariç, anlam bazlı AI incelemesine ver.
    candidate_keys = {(c["campaign_id"], c["ad_group_id"], c["search_term"]) for c in candidates}
    passed_rows = [
        r for r in search_terms
        if (r["campaign_id"], r["ad_group_id"], r["search_term"]) not in candidate_keys
        and not is_exempt_row(r, profile)
    ]
    passed_rows, _ = filter_already_negative(passed_rows, existing_negatives)
    ai_candidates, ai_review_note = review_rows(passed_rows, profile)
    candidates = sorted(candidates + ai_candidates, key=lambda c: c["clicks"], reverse=True)

    candidates, already_negative_count = filter_already_negative(candidates, existing_negatives)

    return {
        "total_terms": len(search_terms),
        "candidates": candidates,
        "already_negative_count": already_negative_count,
        "ai_review_note": ai_review_note,
        "profile_used": getattr(profile, "DISPLAY_NAME", None),
    }


@app.post("/api/apply-negatives")
def api_apply_negatives(body: ApplyNegativesRequest, _auth: bool = Depends(require_auth)):
    if not body.terms:
        raise HTTPException(400, "Hiç terim seçilmedi")
    try:
        result = add_negative_keywords(
            body.customer_id,
            [t.model_dump() for t in body.terms],
            validate_only=body.validate_only,
        )
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(500, str(exc)) from exc
    return result
