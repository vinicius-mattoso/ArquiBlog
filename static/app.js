const bootstrapElement = document.getElementById("bootstrap-data");
const bootstrapData = JSON.parse(bootstrapElement.textContent);

const generationForm = document.getElementById("generation-form");
const settingsForm = document.getElementById("settings-form");
const formStatus = document.getElementById("form-status");
const settingsStatus = document.getElementById("settings-status");
const resultMeta = document.getElementById("result-meta");
const resultContent = document.getElementById("result-content");
const resultImage = document.getElementById("result-image");
const imageInput = document.getElementById("image-input");
const imagePreview = document.getElementById("image-preview");
const historyList = document.getElementById("history-list");
const tabButtons = document.querySelectorAll(".tab-button");
const uploadBox = document.querySelector(".upload-box");

function renderResult(text, metaText, imageUrl = null) {
  resultMeta.textContent = metaText;
  resultContent.textContent = text;
  resultContent.classList.remove("empty-state");

  if (imageUrl) {
    resultImage.innerHTML = `<img src="${imageUrl}" alt="Imagem do projeto">`;
    resultImage.classList.remove("empty-state");
  } else {
    resultImage.textContent = "A imagem enviada aparecerá aqui junto com o texto para avaliação completa.";
    resultImage.classList.add("empty-state");
  }
}

function renderHistoryItem(item) {
  const article = document.createElement("article");
  article.className = "history-card";
  article.dataset.text = item.texto || "";
  article.dataset.meta = `${item.canal_label} - ${item.data_hora}`;
  article.dataset.imageUrl = item.imagem_url || "";
  article.innerHTML = `
    <div class="history-topline">
      <strong>${item.canal_label}</strong>
      <span>${item.data_hora}</span>
    </div>
    <p>${(item.frases || []).filter(Boolean).join(" - ")}</p>
  `;
  article.addEventListener("click", () => {
    renderResult(article.dataset.text, article.dataset.meta, article.dataset.imageUrl);
  });
  return article;
}

function renderHistory(items) {
  historyList.innerHTML = "";
  if (!items.length) {
    historyList.innerHTML = "<p class='status-text'>Nenhuma geração encontrada.</p>";
    return;
  }

  items.forEach((item) => {
    historyList.appendChild(renderHistoryItem(item));
  });
}

async function refreshHistory() {
  const response = await fetch("/api/history");
  const data = await response.json();
  renderHistory(data.items || []);
}

imageInput.addEventListener("change", () => {
  const [file] = imageInput.files;
  if (!file) {
    imagePreview.innerHTML = "<span>Preview da imagem</span>";
    imagePreview.classList.add("is-empty");
    uploadBox.querySelector("em").textContent = "Clique para escolher o arquivo";
    return;
  }

  const url = URL.createObjectURL(file);
  imagePreview.innerHTML = `<img src="${url}" alt="Preview da imagem do projeto">`;
  imagePreview.classList.remove("is-empty");
  uploadBox.querySelector("em").textContent = file.name;
});

generationForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  formStatus.textContent = "Gerando conteúdo editorial...";

  const formData = new FormData(generationForm);
  const response = await fetch("/api/generate", {
    method: "POST",
    body: formData,
  });
  const data = await response.json();

  if (!response.ok) {
    formStatus.textContent = data.error || "Falha ao gerar conteúdo.";
    return;
  }

  formStatus.textContent = data.message;

  if (data.history_item) {
    renderResult(
      data.text,
      `${data.history_item.canal_label} - ${data.history_item.data_hora}`,
      data.history_item.imagem_url
    );
  } else {
    renderResult(data.text, "Conteúdo gerado nesta sessão");
  }

  generationForm.reset();
  imagePreview.innerHTML = "<span>Preview da imagem</span>";
  imagePreview.classList.add("is-empty");
  uploadBox.querySelector("em").textContent = "Clique para escolher o arquivo";
  await refreshHistory();
});

settingsForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  settingsStatus.textContent = "Salvando ajustes...";

  const payload = Object.fromEntries(new FormData(settingsForm).entries());
  const response = await fetch("/api/settings", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(payload),
  });
  const data = await response.json();

  if (!response.ok) {
    settingsStatus.textContent = data.error || "Falha ao salvar ajustes.";
    return;
  }

  settingsStatus.textContent = data.message;
  document.getElementById("brand-tagline").textContent = data.settings.tagline;
  document.getElementById("office-name").textContent = data.settings.office_name;
  document.getElementById("voice-style").textContent = data.settings.voice_style;
  document.getElementById("persona").textContent = data.settings.persona;
  document.getElementById("settings-office-summary").textContent = data.settings.office_name;

  const channelSelect = settingsForm.querySelector('select[name="default_channel"]');
  document.getElementById("settings-channel-summary").textContent =
    channelSelect.options[channelSelect.selectedIndex].textContent;
});

document.getElementById("refresh-history").addEventListener("click", async () => {
  await refreshHistory();
});

document.getElementById("copy-result").addEventListener("click", async () => {
  const text = resultContent.textContent.trim();
if (!text || resultContent.classList.contains("empty-state")) {
    return;
  }

  await navigator.clipboard.writeText(text);
});

document.querySelectorAll(".history-card").forEach((card) => {
  card.addEventListener("click", () => {
    renderResult(card.dataset.text, card.dataset.meta, card.dataset.imageUrl);
  });
});

tabButtons.forEach((button) => {
  button.addEventListener("click", () => {
    tabButtons.forEach((item) => item.classList.remove("is-active"));
    document.querySelectorAll(".tab-panel").forEach((panel) => panel.classList.remove("is-active"));
    button.classList.add("is-active");
    document.getElementById(button.dataset.tabTarget).classList.add("is-active");
  });
});

renderHistory(bootstrapData.history || []);
