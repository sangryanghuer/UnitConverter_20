const form = document.getElementById("convert-form");
const unitSelect = document.getElementById("unit");
const valueInput = document.getElementById("value");
const errorBox = document.getElementById("error");
const resultsSection = document.getElementById("results");
const resultsBody = document.getElementById("results-body");

const UNIT_ORDER = ["meter", "feet", "yard", "cubit"];

const ERROR_MESSAGES = {
  value: "값은 0 이상의 숫자여야 합니다.",
  unit: "등록되지 않은 단위입니다. (meter, feet, yard, cubit)",
  parse: "입력 형식이 올바르지 않습니다.",
};

function hide(el) {
  el.classList.add("hidden");
}

function show(el) {
  el.classList.remove("hidden");
}

function showError(failedFields) {
  const messages = failedFields.map((field) => ERROR_MESSAGES[field] || `오류: ${field}`);
  errorBox.textContent = messages.join(" ");
  show(errorBox);
  hide(resultsSection);
}

function renderResults(conversions, inputUnit) {
  resultsBody.innerHTML = "";

  for (const unit of UNIT_ORDER) {
    const row = document.createElement("tr");
    if (unit === inputUnit) {
      row.classList.add("highlight");
    }

    const unitCell = document.createElement("td");
    unitCell.textContent = unit;

    const valueCell = document.createElement("td");
    valueCell.className = "value";
    valueCell.textContent = conversions[unit].toFixed(4);

    row.append(unitCell, valueCell);
    resultsBody.append(row);
  }

  hide(errorBox);
  show(resultsSection);
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();

  const unit = unitSelect.value;
  const rawValue = valueInput.value.trim();

  if (rawValue === "") {
    showError(["parse"]);
    return;
  }

  const value = Number(rawValue);
  if (Number.isNaN(value)) {
    showError(["parse"]);
    return;
  }

  try {
    const response = await fetch("/api/convert", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ unit, value }),
    });

    if (!response.ok) {
      showError(["parse"]);
      return;
    }

    const result = await response.json();

    if (result.status !== "success") {
      showError(result.failed_fields || ["parse"]);
      return;
    }

    renderResults(result.conversions, unit);
  } catch {
    showError(["parse"]);
  }
});
