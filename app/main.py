import os
import secrets

from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

from app.ads_client import list_accounts, fetch_search_terms
from app.negative_rules import find_candidates
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
        search_terms = fetch_search_terms(body.customer_id, body.date_range)
    except Exception as exc:  # noqa: BLE001
        raise HTTPException(500, str(exc)) from exc

    profile = get_profile(body.customer_id)
    candidates = find_candidates(search_terms, profile=profile)
    return {
        "total_terms": len(search_terms),
        "candidates": candidates,
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
