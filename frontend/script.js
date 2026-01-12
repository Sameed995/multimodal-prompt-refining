const form = document.getElementById("uploadForm");
const statusDiv = document.getElementById("status");
const outputDiv = document.getElementById("output");
const dropZone = document.getElementById("drop-zone");
const fileInput = document.getElementById("files");
const fileList = document.getElementById("file-list");
const resetBtn = document.getElementById("resetBtn");
const toggleViewBtn = document.getElementById("toggleViewBtn");


let selectedFiles = [];
let showJSON = true;

// click to select section
dropZone.addEventListener("click", () => fileInput.click());

fileInput.addEventListener("change", () => {
  addFiles(fileInput.files);
});
// drag and drop files
dropZone.addEventListener("dragover", (e) => {
  e.preventDefault();
  dropZone.classList.add("dragover");
});

dropZone.addEventListener("dragleave", () => {
  dropZone.classList.remove("dragover");
});

dropZone.addEventListener("drop", (e) => {
  e.preventDefault();
  dropZone.classList.remove("dragover");
  addFiles(e.dataTransfer.files);
});
toggleViewBtn.addEventListener("click", () => {
  showJSON = !showJSON;
  toggleViewBtn.textContent = showJSON ? "Show Cards" : "Show JSON";
  renderResults(lastResults); 
});

let lastResults = []; 


function addFiles(files) {
  for (const file of files) {
    // Avoid duplicate filenames
    if (!selectedFiles.some(f => f.name === file.name && f.size === file.size)) {
      selectedFiles.push(file);
    }
  }
  renderFileList();
}

function renderFileList() {
  fileList.innerHTML = "";

  selectedFiles.forEach((file, index) => {
    const li = document.createElement("li");
    li.className = "file-item";

    // Image thumbnail
    if (file.type.startsWith("image/")) {
      const img = document.createElement("img");
      img.className = "file-thumb";
      img.src = URL.createObjectURL(file);
      img.alt = file.name;
      li.appendChild(img);
    }

    // Filename
    const span = document.createElement("span");
    span.className = "file-name-text";
    span.textContent = file.name;
    li.appendChild(span);

    // Remove button
    const removeBtn = document.createElement("button");
    removeBtn.type = "button";
    removeBtn.textContent = "×";
    removeBtn.className = "remove-btn";
    removeBtn.addEventListener("click", () => {
      selectedFiles.splice(index, 1);
      renderFileList();
    });
    li.appendChild(removeBtn);

    fileList.appendChild(li);
  });
}

// submit section
form.addEventListener("submit", async (e) => {
  e.preventDefault();

  if (selectedFiles.length === 0) {
    statusDiv.textContent = "Please select at least one file.";
    return;
  }

  const formData = new FormData();
  selectedFiles.forEach(file => formData.append("files", file));

  statusDiv.textContent = "Uploading and refining...";
  outputDiv.innerHTML = "";

  try {
    const response = await fetch("http://127.0.0.1:8000/refine-prompt", {
      method: "POST",
      body: formData,
    });

 
    const data = await response.json();
    console.log("Parsed JSON:", data);
    statusDiv.textContent = "Refinement complete";
    lastResults = data.results;
    renderResults(data.results);

  } catch (error) {
    statusDiv.textContent = "Error occurred ❌";
    outputDiv.textContent = error.toString();
  }
});

// reset section
resetBtn.addEventListener("click", () => {
  selectedFiles = [];
  fileList.innerHTML = "";
  outputDiv.innerHTML = "";
  statusDiv.textContent = "";
  fileInput.value = "";
  statusDiv.textContent = "Ready for new upload";
});

// rendering of output cards
function renderResults(results) {
  outputDiv.innerHTML = "";

  if (showJSON) {
  const jsonCard = document.createElement("div");
  jsonCard.className = "output-card json-view";
  jsonCard.innerHTML = `<pre>${JSON.stringify(results, null, 2)}</pre>`;
  outputDiv.appendChild(jsonCard);
  return;
}


  // show card view
  results.forEach(item => {
    const card = document.createElement("div");
    card.className = "output-card";

    card.innerHTML = `
      <div class="output-header">
        <div class="file-name">${item.filename}</div>
        <div class="file-type">${item.file_type}</div>
      </div>

      <div class="section">
        <div class="section-title">Core Intent</div>
        <div class="intent">${item.refined_prompt.core_intent || "—"}</div>
      </div>

      <div class="section">
        <div class="section-title">Functional Requirements</div>
        <ul>
          ${(item.refined_prompt.functional_requirements || [])
            .map(r => `<li>${r}</li>`).join("") || "<li>—</li>"}
        </ul>
      </div>

      <div class="section">
        <div class="section-title">Technical Constraints</div>
        <ul>
          ${(item.refined_prompt.technical_constraints || [])
            .map(r => `<li>${r}</li>`).join("") || "<li>—</li>"}
        </ul>
      </div>

      <div class="section">
        <div class="section-title">Expected Output</div>
        <ul>
          ${(item.refined_prompt.expected_output.length > 0
              ? item.refined_prompt.expected_output.map(r => `<li>${r}</li>`).join("")
              : "<li>—</li>")}
        </ul>
      </div>

      <div class="section missing">
        <div class="section-title">Missing Information</div>
        <ul>
          ${(item.refined_prompt.missing_information.length > 0
              ? item.refined_prompt.missing_information.map(r => `<li>${r}</li>`).join("")
              : "<li>—</li>")}
        </ul>
      </div>
    `;

    outputDiv.appendChild(card);
  });
}

