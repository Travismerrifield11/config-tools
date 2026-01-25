// vrf.js

const allVrfs = ["2WR","AMI","FWBB","GAS","IPCAM","MGMT","PEER","PHYSEC","SUB"];

const vrfMasks = {
  "2WR": "255.255.255.240",
  "AMI": "255.255.255.240",
  "FWBB": "255.255.255.240",
  "GAS": "255.255.255.248",
  "IPCAM": "255.255.255.240",
  "MGMT": "255.255.255.240",
  "PEER": "255.255.255.248",
  "PHYSEC": "255.255.255.248"
};

const tableBody = document.querySelector("#vrfTable tbody");
const addBtn = document.getElementById("addVrf");

// Updates all VRF dropdowns to prevent duplicate selections
function updateDropdowns() {
  const selected = [...document.querySelectorAll(".vrf-select")]
    .map(s => s.value)
    .filter(v => v);

  document.querySelectorAll(".vrf-select").forEach(sel => {
    const current = sel.value;
    sel.innerHTML =
      `<option value="">Select...</option>` +
      allVrfs
        .filter(v => v === current || !selected.includes(v))
        .map(v => `<option value="${v}">${v}</option>`)
        .join("");
    sel.value = current;
  });
}

// Handles a VRF selection change and updates the subnet mask
function handleVrfChange(select, maskCell) {
  const vrf = select.value;
  maskCell.innerHTML = "";

  if (!vrf) return;

  if (vrf === "SUB") {
    maskCell.innerHTML =
      '<select class="subnet-mask">' +
      '<option value="255.255.255.248">255.255.255.248</option>' +
      '<option value="255.255.255.240">255.255.255.240</option>' +
      '<option value="255.255.255.192">255.255.255.192</option>' +
      '</select>';
  } else {
    maskCell.innerHTML = `<input type="text" value="${vrfMasks[vrf]}" readonly>`;
  }

  updateDropdowns();
}

// Adds a new row to the VRF table
function addRow() {
  const row = document.createElement("tr");

  row.innerHTML =
    '<td>' +
      '<select class="vrf-select">' +
        '<option value="">Select...</option>' +
        allVrfs.map(v => `<option value="${v}">${v}</option>`).join("") +
      '</select>' +
    '</td>' +
    '<td><input type="text" placeholder="Default Gateway"></td>' +
    '<td class="mask-cell"></td>' +
    '<td><button class="remove">Remove</button></td>';

  const vrfSelect = row.querySelector(".vrf-select");
  const maskCell = row.querySelector(".mask-cell");
  const removeBtn = row.querySelector(".remove");

  vrfSelect.addEventListener("change", () => handleVrfChange(vrfSelect, maskCell));
  removeBtn.addEventListener("click", () => {
    row.remove();
    updateDropdowns();
  });

  tableBody.appendChild(row);
  updateDropdowns();
}

addBtn.addEventListener("click", addRow);
