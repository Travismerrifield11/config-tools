// ================= CONFIG AREA JS =================
document.addEventListener("DOMContentLoaded", () => {

    // ----------------- CORE SECTION -----------------
    // existing core code unchanged
    console.log("Core JS loaded");

    // ----------------- WAN SECTION -----------------
    // existing WAN code unchanged
    console.log("WAN JS loaded");

    // ================= VRF SECTION =================
    console.log("VRF JS loaded");

    // Add VRF
    const addVrfBtn = document.getElementById("addVrf");
    addVrfBtn?.addEventListener("click", () => {
        console.log("Add VRF clicked");
        const select = document.getElementById("vrfSelect");
        const vrfName = select?.value.trim();
        if (!vrfName) {
            alert("Please select a VRF to add.");
            return;
        }

        const tableBody = document.querySelector("#vrfTable tbody");
        if (!tableBody) return;

        // Prevent duplicates
        if (Array.from(tableBody.querySelectorAll("tr")).some(r => r.dataset.vrf === vrfName)) {
            alert(`VRF ${vrfName} has already been added.`);
            return;
        }

        const row = document.createElement("tr");
        row.dataset.vrf = vrfName;

        // Subnet mask field
        let subnetField = "";
        const readonlyVrfs = ["2WR", "AMI", "FWBB", "GAS", "IPCAM", "MGMT", "PEER", "PHYSEC"];
        if (readonlyVrfs.includes(vrfName)) {
            subnetField = `<input type="text" class="vrf-subnetmask" value="255.255.255.240" readonly>`;
        } else if (vrfName === "SUB") {
            subnetField = `
                <select class="subnet-mask">
                    <option value="255.255.255.248">255.255.255.248</option>
                    <option value="255.255.255.240" selected>255.255.255.240</option>
                    <option value="255.255.255.192">255.255.255.192</option>
                </select>
            `;
        } else {
            subnetField = `<input type="text" class="vrf-subnetmask" value="255.255.255.240" readonly>`;
        }

        row.innerHTML = `
            <td>${vrfName}</td>
            <td><input type="text" class="vrf-default-gateway" placeholder="Default Gateway"></td>
            <td>${subnetField}</td>
            <td><button class="btn-remove">Remove</button></td>
        `;

        tableBody.appendChild(row);

        row.querySelector(".btn-remove")?.addEventListener("click", () => row.remove());

        select.value = "";
    });

    // Function to collect VRF data
    function collectVrfData() {
        const rows = document.querySelectorAll("#vrfTable tbody tr");
        const data = [];

        rows.forEach(row => {
            const gatewayInput = row.querySelector(".vrf-default-gateway");
            if (!gatewayInput || !gatewayInput.value.trim()) return; // skip incomplete

            let subnetmask = row.querySelector(".vrf-subnetmask")?.value;
            if (!subnetmask) {
                subnetmask = row.querySelector(".subnet-mask")?.value;
            }
            subnetmask = subnetmask || "255.255.255.240";

            data.push({
                network: row.dataset.vrf,
                default_gateway: gatewayInput.value.trim(),
                subnetmask: subnetmask.trim()
            });
        });

        return data;
    }

    // Generate VRF
    const genVrfBtn = document.getElementById("generate-vrf");
    genVrfBtn?.addEventListener("click", () => {
        console.log("Generate VRF clicked");

        const vrfs = collectVrfData();
        console.log("=== VRFs collected ===", vrfs);

        if (!vrfs.length) {
            alert("Please enter a default gateway for every VRF.");
            return;
        }

        console.log("Sending VRF payload to backend...");
        fetch("/update_vrf", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(vrfs)
        })
        .then(res => res.json())
        .then(data => {
            console.log("Response from backend:", data);
            updateConfigOutput(data);
        })
        .catch(err => console.error("Error generating VRFs:", err));
    });

}); // end DOMContentLoaded








// ====================== PORTS ======================
function collectPortsData() {
    const rows = document.querySelectorAll("#ports-table tbody tr");
    const data = [];

    rows.forEach(row => {
        const iface = row.querySelector(".port-interface")?.value;
        const ip = row.querySelector(".port-ip")?.value;
        const desc = row.querySelector(".port-desc")?.value;
        const media_type = row.querySelector(".port-media")?.value;

        if (iface || ip || desc || media_type) {
            data.push({
                interface: iface,
                ip,
                description: desc,
                media_type
            });
        }
    });

    return data;
}

document.getElementById("generate-ports")?.addEventListener("click", async () => {
    try {
        window.configPorts = await fetchSection("/generate/ports", collectPortsData());
        updateConfigOutput();
    } catch (err) {
        alert(err.message);
    }
});
});
