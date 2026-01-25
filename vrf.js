const allVrfs = [
  "2WR","AMI","FWBB","GAS","IPCAM","MGMT","PEER","PHYSEC","SUB"
];

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
const vrfSelect = document.getElementById("vrfSelect");

function updateAvailableVrfs() {
    const added = [...tableBody.querySelectorAll("tr td:first-child")].map(td => td.textContent);
    Array.from(vrfSelect.options).forEach(opt => {
        opt.disabled = opt.value && added.includes(opt.value);
    });
}

function handleVrfChange(maskCell, vrf) {
    maskCell.innerHTML = "";
    if (!vrf) return;

    if (vrf === "SUB") {
        maskCell.innerHTML = `
            <select class="subnet-mask">
                <option value="255.255.255.248">255.255.255.248</option>
                <option value="255.255.255.240">255.255.255.240</option>
                <option value="255.255.255.192">255.255.255.192</option>
            </select>
        `;
    } else {
        maskCell.innerHTML = `<input type="text" value="${vrfMasks[vrf]}" readonly>`;
    }
}

function addRow() {
    const vrfValue = vrfSelect.value;
    if (!vrfValue) return;

    // create row
    const row = document.createElement("tr");
    row.innerHTML = `
        <td>${vrfValue}</td>
        <td><input type="text" placeholder="Default Gateway"></td>
        <td class="mask-cell"></td>
        <td><button class="btn-remove">Remove</button></td>
    `;

    const maskCell = row.querySelector(".mask-cell");
    const removeBtn = row.querySelector(".btn-remove");

    handleVrfChange(maskCell, vrfValue);

    removeBtn.addEventListener("click", () => {
        row.remove();
        updateAvailableVrfs();
    });

    tableBody.appendChild(row);
    updateAvailableVrfs();
    vrfSelect.value = "";
}

addBtn.addEventListener("click", addRow);
