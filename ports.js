document.addEventListener("DOMContentLoaded", () => {
    // ----------------------------
    // VRF Options
    // ----------------------------
    const vrfOptions = [
        "2WR","AMI","FWBB","GAS","IPCAM","MGMT","PEER","PHYSEC","SUB"
    ];

    // ----------------------------
    // Port Options
    // ----------------------------
    const portOptions = Array.from({ length: 12 }, (_, i) => `Gi 0/0/${i}`);

    // ----------------------------
    // Table and Button References
    // ----------------------------
    const tableBody = document.querySelector("#portTable tbody");
    const addBtn = document.getElementById("addPort");
    const portSelect = document.getElementById("portSelect"); // We'll create a select in HTML for port choices

    // ----------------------------
    // Media Type Logic
    // ----------------------------
    function getMediaType(portName) {
        const index = parseInt(portName.split("/").pop());
        if (index >= 0 && index <= 3) return "Copper";
        if (index >= 4 && index <= 7) return ""; // user-selectable
        if (index >= 8 && index <= 11) return "SFP";
        return "";
    }

    // ----------------------------
    // Add a new row
    // ----------------------------
    function addRow() {
        const selectedPort = portSelect.value;
        if (!selectedPort) {
            alert("Please select a port to add.");
            return;
        }

        // Prevent adding the same port twice
        const existingPorts = Array.from(tableBody.querySelectorAll("td:first-child")).map(td => td.textContent);
        if (existingPorts.includes(selectedPort)) {
            alert(`${selectedPort} is already added.`);
            return;
        }

        const row = document.createElement("tr");

        // Build VRF options for this row
        const vrfSelectOptions = vrfOptions.map(v => `<option value="${v}">${v}</option>`).join("");

        // Build Media Type input
        const mediaTypeValue = getMediaType(selectedPort);
        const mediaTypeInput = (mediaTypeValue === "")
            ? `<select class="media-type">
                    <option value="Copper">Copper</option>
                    <option value="SFP">SFP</option>
               </select>`
            : `<input type="text" value="${mediaTypeValue}" readonly>`;

        // Row HTML
        row.innerHTML = `
            <td>${selectedPort}</td>
            <td><input type="text" placeholder="Description"></td>
            <td>
                <select class="vrf-select">
                    <option value="">Select...</option>
                    ${vrfSelectOptions}
                </select>
            </td>
            <td>${mediaTypeInput}</td>
            <td><button class="remove">Remove</button></td>
        `;

        // Remove button
        row.querySelector(".remove").addEventListener("click", () => {
            row.remove();
        });

        tableBody.appendChild(row);
    }

    // ----------------------------
    // Add Button Click Event
    // ----------------------------
    addBtn.addEventListener("click", addRow);
});
