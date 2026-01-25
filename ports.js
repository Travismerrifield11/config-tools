// ports.js

const allPorts = [
  "Gi 0/0/0","Gi 0/0/1","Gi 0/0/2","Gi 0/0/3",
  "Gi 0/0/4","Gi 0/0/5","Gi 0/0/6","Gi 0/0/7",
  "Gi 0/0/8","Gi 0/0/9","Gi 0/0/10","Gi 0/0/11"
];

const allVrfs = ["2WR","AMI","FWBB","GAS","IPCAM","MGMT","PEER","PHYSEC","SUB"];

const tableBody = document.querySelector("#portTable tbody");
const addBtn = document.getElementById("addPort");

// Determine the media type options for each port
function getMediaTypeOptions(port) {
  if (["Gi 0/0/0","Gi 0/0/1","Gi 0/0/2","Gi 0/0/3"].includes(port)) {
    return '<input type="text" value="Copper" readonly>';
  } else if (["Gi 0/0/4","Gi 0/0/5","Gi 0/0/6","Gi 0/0/7"].includes(port)) {
    return '<select class="media-type">' +
      '<option value="Copper">Copper</option>' +
      '<option value="SFP">SFP</option>' +
      '</select>';
  } else { // 8-11
    return '<input type="text" value="SFP" readonly>';
  }
}

// Updates VRF dropdowns in all rows (prevents duplicates if desired)
function updateVrfDropdowns() {
  const selected = [...document.querySelectorAll(".vrf-select")]
    .map(s => s.value)
    .filter(v => v);

  document.querySelectorAll(".vrf-select").forEach(sel => {
    const current = sel.value;
    sel.innerHTML =
      '<option value="">Select...</option>' +
      allVrfs
        .filter(v => v === current || !selected.includes(v))
        .map(v => `<option value="${v}">${v}</option>`)
        .join("");
    sel.value = current;
  });
}

// Adds a new row to the Ports table
function addRow() {
  const row = document.createElement("tr");

  // Only allow ports that haven’t been added yet
  const usedPorts = [...document.querySelectorAll(".port-label")].map(p => p.textContent);
  const availablePorts = allPorts.filter(p => !usedPorts.includes(p));
  if (availablePorts.length === 0) return;

  const port = availablePorts[0];

  row.innerHTML =
    `<td class="port-label">${port}</td>` +
    `<td><input type="text" placeholder="Description"></td>` +
    `<td>` +
      `<select class="vrf-select">` +
        `<option value="">Select...</option>` +
        allVrfs.map(v => `<option value="${v}">${v}</option>`).join("") +
      `</select>` +
    `</td>` +
    `<td class="media-cell">${getMediaTypeOptions(port)}</td>` +
    `<td><button class="remove">Remove</button></td>`;

  const vrfSelect = row.querySelector(".vrf-select");
  const removeBtn = row.querySelector(".remove");

  vrfSelect.addEventListener("change", updateVrfDropdowns);

  removeBtn.addEventListener("click", () => {
    row.remove();
    updateVrfDropdowns();
  });

  tableBody.appendChild(row);
  updateVrfDropdowns();
}

addBtn.addEventListener("click", addRow);
