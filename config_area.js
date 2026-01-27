// ===================== CONFIG AREA SCRIPT =====================
document.addEventListener("DOMContentLoaded", () => {
// --------------------- Memory Storage ---------------------
window.configCore = "";
window.configWan = "";
window.configVrf = "";
window.configPorts = "";

// --------------------- Update Textarea ---------------------
function updateConfigOutput() {
    let combined = "";

    if (document.getElementById("toggle-core")?.checked && window.configCore)
        combined += window.configCore + "\n\n";

    if (document.getElementById("toggle-wan")?.checked && window.configWan)
        combined += window.configWan + "\n\n";

    if (document.getElementById("toggle-vrf")?.checked && window.configVrf)
        combined += window.configVrf + "\n\n";

    if (document.getElementById("toggle-ports")?.checked && window.configPorts)
        combined += window.configPorts + "\n\n";

    document.getElementById("config-output").value = combined.trim();
}

// --------------------- Toggle Listeners ---------------------
["toggle-core", "toggle-wan", "toggle-vrf", "toggle-ports"].forEach(id => {
    document.getElementById(id)?.addEventListener("change", updateConfigOutput);
});

// --------------------- POST Helper ---------------------
async function fetchSection(endpoint, payload) {
    const response = await fetch(`http://127.0.0.1:5000${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    });

    if (!response.ok) {
        throw new Error(`Failed request to ${endpoint}`);
    }

    const data = await response.json();
    return data.config;
}

// ====================== CORE ======================
document.getElementById("generate-core")?.addEventListener("click", async () => {
	console.log("VRF JS loaded and DOM ready"); // <-- check if script runs
    const payload = {
        hostname: document.getElementById("hostname")?.value.trim(),
        loopback0: document.getElementById("loopback0")?.value.trim(),
        loopback1: document.getElementById("loopback1")?.value.trim(),
        hub_slice: document.getElementById("hub_slice")?.value,
        city: document.getElementById("city")?.value.trim(),
        state: document.getElementById("state")?.value,
        location_type: document.getElementById("location_type")?.value
    };

    try {
        window.configCore = await fetchSection("/generate/core", payload);
        updateConfigOutput();
    } catch (err) {
        alert(err.message);
    }
});

// ====================== WAN ======================
function collectWanData() {
    const rows = document.querySelectorAll("#wan-table tbody tr");
    const data = [];

    rows.forEach(row => {
        const circuit = row.querySelector(".wan-circuit")?.value;
        const ip = row.querySelector(".wan-ip")?.value;
        const bandwidth = row.querySelector(".wan-bandwidth")?.value;
        const media_type = row.querySelector(".wan-media")?.value;

        if (circuit || ip || bandwidth || media_type) {
            data.push({ circuit, ip, bandwidth, media_type });
        }
    });

    return data;
}

document.getElementById("generate-wan")?.addEventListener("click", async () => {
    try {
        window.configWan = await fetchSection("/generate/wan", collectWanData());
        updateConfigOutput();
    } catch (err) {
        alert(err.message);
    }
});

// ================= VRF SECTION =================
document.addEventListener("DOMContentLoaded", () => {
console.log("VRF JS loaded and DOM ready"); // <-- check if script runs

    // Add VRF
    document.getElementById("addVrf").addEventListener("click", () => {
        const select = document.getElementById("vrfSelect");
        const vrfName = select.value.trim();

        if (!vrfName) {
            alert("Please select a VRF to add.");
            return;
        }

        const tableBody = document.querySelector("#vrfTable tbody");

        // Prevent duplicate VRFs
        if (Array.from(tableBody.querySelectorAll("tr")).some(row => row.dataset.vrf === vrfName)) {
            alert(`VRF ${vrfName} has already been added.`);
            return;
        }

        const row = document.createElement("tr");
        row.dataset.vrf = vrfName;

        // Determine subnet mask input type
        let subnetField = "";
        const readonlyVrfs = ["2WR", "AMI", "FWBB", "GAS", "IPCAM", "MGMT", "PEER", "PHYSEC"];
        if (readonlyVrfs.includes(vrfName)) {
            // Fixed subnet mask input
            subnetField = `<input type="text" class="vrf-subnetmask" value="255.255.255.240" readonly>`;
        } else if (vrfName === "SUB") {
            // Dropdown select for subnet mask
            subnetField = `
                <select class="subnet-mask">
                    <option value="255.255.255.248">255.255.255.248</option>
                    <option value="255.255.255.240" selected>255.255.255.240</option>
                    <option value="255.255.255.192">255.255.255.192</option>
                </select>
            `;
        } else {
            // Default to read-only 255.255.255.240
            subnetField = `<input type="text" class="vrf-subnetmask" value="255.255.255.240" readonly>`;
        }

        row.innerHTML = `
            <td>${vrfName}</td>
            <td><input type="text" class="vrf-default-gateway" placeholder="Default Gateway"></td>
            <td>${subnetField}</td>
            <td><button class="btn-remove">Remove</button></td>
        `;

        tableBody.appendChild(row);

        // Remove button
        row.querySelector(".btn-remove").addEventListener("click", () => row.remove());

        // Reset dropdown
        select.value = "";
    });

    // Collect VRF data from table
    function collectVrfData() {
        return Array.from(document.querySelectorAll("#vrfTable tbody tr"))
            .map(row => {
                const gatewayInput = row.querySelector(".vrf-default-gateway");
                if (!gatewayInput || !gatewayInput.value.trim()) return null;

                // Determine subnet mask
                let subnetmask = row.querySelector(".vrf-subnetmask")?.value.trim();
                if (!subnetmask) {
                    subnetmask = row.querySelector(".subnet-mask")?.value;
                }
                subnetmask = subnetmask || "255.255.255.240";

                return {
                    network: row.dataset.vrf,
                    default_gateway: gatewayInput.value.trim(),
                    subnetmask
                };
            })
            .filter(vrf => vrf); // Remove rows missing default gateway
    }

    // Generate VRF
	document.getElementById("generate-vrf").addEventListener("click", () => {
    const vrfs = collectVrfData();

    console.log("=== VRFs collected ===");
    console.log(vrfs);

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
});







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
