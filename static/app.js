const accountSelect = document.getElementById("account");
const dateRangeSelect = document.getElementById("date-range");
const customDateFields = document.getElementById("custom-date-fields");
const startDateInput = document.getElementById("start-date");
const endDateInput = document.getElementById("end-date");
const analyzeBtn = document.getElementById("analyze-btn");
const applyBtn = document.getElementById("apply-btn");
const statusEl = document.getElementById("status");
const resultsSection = document.getElementById("results");
const resultsBody = document.getElementById("results-body");
const resultsSummary = document.getElementById("results-summary");
const selectAllCheckbox = document.getElementById("select-all");
const lastCheckedSection = document.getElementById("last-checked");
const lastCheckedText = document.getElementById("last-checked-text");
const sinceLastCheckedBtn = document.getElementById("since-last-checked-btn");

let currentCandidates = [];

function lastCheckedKey(customerId) {
  return `lastChecked:${customerId}`;
}

function todayIso() {
  return new Date().toISOString().slice(0, 10);
}

function getLastChecked(customerId) {
  try {
    return localStorage.getItem(lastCheckedKey(customerId));
  } catch {
    return null;
  }
}

function setLastChecked(customerId, isoDate) {
  try {
    localStorage.setItem(lastCheckedKey(customerId), isoDate);
  } catch {
    // localStorage yoksa (gizli sekme vb.) sessizce yok say
  }
}

function daysAgo(isoDate) {
  const diffMs = new Date(todayIso()) - new Date(isoDate);
  return Math.round(diffMs / 86400000);
}

function refreshLastCheckedInfo() {
  const customerId = accountSelect.value;
  if (!customerId) {
    lastCheckedSection.hidden = true;
    return;
  }
  const lastChecked = getLastChecked(customerId);
  lastCheckedSection.hidden = false;
  if (!lastChecked) {
    lastCheckedText.textContent = "Bu hesap için henüz kontrol kaydı yok.";
    sinceLastCheckedBtn.disabled = true;
  } else {
    const n = daysAgo(lastChecked);
    const label = n <= 0 ? "bugün" : n === 1 ? "1 gün önce" : `${n} gün önce`;
    lastCheckedText.textContent = `Son kontrol: ${label} (${lastChecked})`;
    sinceLastCheckedBtn.disabled = false;
  }
}

function updateCustomDateVisibility() {
  customDateFields.hidden = dateRangeSelect.value !== "CUSTOM";
}

dateRangeSelect.addEventListener("change", updateCustomDateVisibility);
accountSelect.addEventListener("change", refreshLastCheckedInfo);

sinceLastCheckedBtn.addEventListener("click", () => {
  const customerId = accountSelect.value;
  const lastChecked = getLastChecked(customerId);
  if (!lastChecked) return;
  dateRangeSelect.value = "CUSTOM";
  updateCustomDateVisibility();
  startDateInput.value = lastChecked;
  endDateInput.value = todayIso();
});

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
    refreshLastCheckedInfo();
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

  const body = { customer_id: customerId, date_range: dateRangeSelect.value };
  if (dateRangeSelect.value === "CUSTOM") {
    if (!startDateInput.value || !endDateInput.value) {
      setStatus("Özel aralık için başlangıç ve bitiş tarihi seç.", true);
      return;
    }
    body.start_date = startDateInput.value;
    body.end_date = endDateInput.value;
  }

  analyzeBtn.disabled = true;
  setStatus("Arama terimleri analiz ediliyor, bu biraz sürebilir...");
  resultsSection.hidden = true;
  try {
    const res = await fetch("/api/analyze", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(body),
    });
    if (!res.ok) throw new Error(await res.text());
    const data = await res.json();
    const profileNote = data.profile_used
      ? `Profil: ${data.profile_used}`
      : "Bu hesap için özel profil tanımlı değil, sadece genel kurallar uygulandı.";
    const alreadyNegativeNote = data.already_negative_count
      ? ` (${data.already_negative_count} terim zaten negatif eklenmişti, tekrar önerilmedi.)`
      : "";
    resultsSummary.textContent = `${data.total_terms} toplam arama teriminden ${data.candidates.length} negatif aday bulundu. ${profileNote}${alreadyNegativeNote}`;
    renderCandidates(data.candidates);
    setStatus("Analiz tamamlandı.");
    setLastChecked(customerId, todayIso());
    refreshLastCheckedInfo();
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
