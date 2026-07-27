const accountSelect = document.getElementById("account");
const dateRangeSelect = document.getElementById("date-range");
const minClicksInput = document.getElementById("min-clicks");
const minCostInput = document.getElementById("min-cost");
const analyzeBtn = document.getElementById("analyze-btn");
const applyBtn = document.getElementById("apply-btn");
const statusEl = document.getElementById("status");
const resultsSection = document.getElementById("results");
const resultsBody = document.getElementById("results-body");
const resultsSummary = document.getElementById("results-summary");
const selectAllCheckbox = document.getElementById("select-all");

let currentCandidates = [];

function setStatus(msg, isError = false) {
  statusEl.textContent = msg;
  statusEl.style.color = isError ? "#d93025" : "";
}

async function loadAccounts() {
  setStatus("Hesaplar yükleniyor...");
  try {
    const res = await fetch("/api/accounts");
    if (!res.ok) throw new Error(await res.text());
    const data = await res.json();
    accountSelect.innerHTML = data.accounts
      .map((a) => `<option value="${a.id}">${a.name} (${a.id})</option>`)
      .join("");
    setStatus(`${data.accounts.length} hesap bulundu.`);
  } catch (err) {
    setStatus(`Hesaplar yüklenemedi: ${err.message}`, true);
  }
}

function renderCandidates(candidates) {
  currentCandidates = candidates;
  resultsBody.innerHTML = candidates
    .map(
      (c, i) => `
      <tr>
        <td><input type="checkbox" class="row-check" data-idx="${i}" /></td>
        <td>${escapeHtml(c.search_term)}</td>
        <td>${escapeHtml(c.campaign_name)}</td>
        <td>${escapeHtml(c.ad_group_name)}</td>
        <td>${c.clicks}</td>
        <td>${c.cost.toFixed(2)}</td>
        <td>${c.conversions}</td>
        <td class="reasons">${c.reasons.map(escapeHtml).join("<br />")}</td>
      </tr>`
    )
    .join("");
  resultsSection.hidden = candidates.length === 0;
  updateApplyButton();
}

function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

function getSelectedCandidates() {
  const checked = Array.from(document.querySelectorAll(".row-check:checked"));
  return checked.map((el) => currentCandidates[Number(el.dataset.idx)]);
}

function updateApplyButton() {
  applyBtn.disabled = getSelectedCandidates().length === 0;
}

analyzeBtn.addEventListener("click", async () => {
  const customerId = accountSelect.value;
  if (!customerId) {
    setStatus("Önce bir hesap seç.", true);
    return;
  }
  analyzeBtn.disabled = true;
  setStatus("Arama terimleri analiz ediliyor, bu biraz sürebilir...");
  resultsSection.hidden = true;
  try {
    const res = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        customer_id: customerId,
        date_range: dateRangeSelect.value,
        min_clicks_zero_conv: Number(minClicksInput.value),
        min_cost_zero_conv: Number(minCostInput.value),
      }),
    });
    if (!res.ok) throw new Error(await res.text());
    const data = await res.json();
    resultsSummary.textContent = `${data.total_terms} toplam arama teriminden ${data.candidates.length} negatif aday bulundu.`;
    renderCandidates(data.candidates);
    setStatus("Analiz tamamlandı.");
  } catch (err) {
    setStatus(`Analiz başarısız: ${err.message}`, true);
  } finally {
    analyzeBtn.disabled = false;
  }
});

resultsBody.addEventListener("change", (e) => {
  if (e.target.classList.contains("row-check")) updateApplyButton();
});

selectAllCheckbox.addEventListener("change", () => {
  document
    .querySelectorAll(".row-check")
    .forEach((el) => (el.checked = selectAllCheckbox.checked));
  updateApplyButton();
});

applyBtn.addEventListener("click", async () => {
  const selected = getSelectedCandidates();
  if (selected.length === 0) return;

  const confirmed = window.confirm(
    `${selected.length} arama terimi negatif anahtar kelime olarak eklenecek. Önce doğrulama (dry-run) yapılacak, ardından onayınla gerçek hesaba yazılacak. Devam edilsin mi?`
  );
  if (!confirmed) return;

  const customerId = accountSelect.value;
  const terms = selected.map((c) => ({
    campaign_id: c.campaign_id,
    search_term: c.search_term,
  }));

  applyBtn.disabled = true;
  setStatus("Doğrulanıyor (dry-run)...");
  try {
    const validateRes = await fetch("/api/apply-negatives", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ customer_id: customerId, terms, validate_only: true }),
    });
    if (!validateRes.ok) throw new Error(await validateRes.text());

    const finalConfirm = window.confirm(
      `Doğrulama başarılı. ${selected.length} negatif anahtar kelime GERÇEK hesaba yazılacak. Bu işlem geri alınabilir ama kampanyanı etkiler. Onaylıyor musun?`
    );
    if (!finalConfirm) {
      setStatus("İşlem iptal edildi.");
      applyBtn.disabled = false;
      return;
    }

    setStatus("Hesaba yazılıyor...");
    const applyRes = await fetch("/api/apply-negatives", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ customer_id: customerId, terms, validate_only: false }),
    });
    if (!applyRes.ok) throw new Error(await applyRes.text());
    const result = await applyRes.json();
    setStatus(`${result.added} negatif anahtar kelime başarıyla eklendi.`);
  } catch (err) {
    setStatus(`İşlem başarısız: ${err.message}`, true);
  } finally {
    updateApplyButton();
  }
});

loadAccounts();
