// -------------------- Ports.js --------------------

// Available ports
const allPorts = [
  "Gi 0/0/0", "Gi 0/0/1", "Gi 0/0/2", "Gi 0/0/3",
  "Gi 0/0/4", "Gi 0/0/5", "Gi 0/0/6", "Gi 0/0/7",
  "Gi 0/0/8", "Gi 0/0/9", "Gi 0/0/10", "Gi 0/0/11"
];

// Available VRFs (reuse from vrf.js)
const vrfOptions = [
  "2WR","AMI","FWBB","GAS","IPCAM","MGMT","PEER","PHYSEC","SUB"
];

// Table body and add button
const portTableBody = document.querySelector("#portTable tbody");
const addPortBtn = document.getElementById("addPort");
const selectPortDropdown = document.getElementById("selectPort");

// Populate the port dropdown
function populatePortDropdown() {
  const usedPorts = [...portTableBody.querySelectorAll(".port-name")].map(td => td.textContent);
  selectPortDropdown.innerHTML = `<option value="">Select...</option>` +
    allPorts.map(port => 
      `<option value="${port}" ${usedPorts.includes(port) ? "disabled" : ""}>${port}</option>`
    ).join("");
}

populatePortDropdown();

// Function to add a new port row
function addPortRow() {
  const selectedPort = selectPortDropdown.value;
  if (!selectedPort) return;

  // Create row
  const row = document.createElement("tr");
  row.innerHTML = `
    <td class="port-name">${selectedPort}</td>
    <td><input type="text" placeholder="Description"></td>
    <td>
      <select class="vrf-select">
        <option value="">Select...</option>
        ${vrfOptions.map(v => `<option value="${v}">${v}</option>`).join("")}
      </select>
    </td>
    <td>
      <select class="media-select">
        ${["Gi 0/0/0","Gi 0/0/1","Gi 0/0/2","Gi 0/0/3"].includes(selectedPort) ? 
          `<option value="Copper">Copper</option>` : ""}
        ${["Gi 0/0/4","Gi 0/0/5","Gi 0/0/6","Gi 0/0/7"].includes(selectedPort) ? 
          `<option value="Copper">Copper</option><option value="SFP">SFP</option>` : ""}
        ${["Gi 0/0/8","Gi 0/0/9","Gi 0/0/10","Gi 0/0/11"].includes(selectedPort) ? 
          `<option value="SFP">SFP</option>` : ""}
      </select>
    </td>
		<td><button class="btn-remove">Remove</button></td>
  `;

	// Remove button functionality
	const removeBtn = row.querySelector(".btn-remove");

	if (removeBtn) {
	  removeBtn.addEventListener("click", () => {
		row.remove();
		populatePortDropdown();
	  });
	}

  portTableBody.appendChild(row);
  selectPortDropdown.value = "";
  populatePortDropdown();
}

// Add button event
addPortBtn.addEventListener("click", addPortRow);
