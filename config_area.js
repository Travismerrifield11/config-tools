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

// ====================== VRF ======================
function collectVrfData() {
    const rows = document.querySelectorAll("#vrf-table tbody tr");
    const data = [];

    rows.forEach(row => {
        const name = row.querySelector(".vrf-name")?.value;
        const rd = row.querySelector(".vrf-rd")?.value;
        const rt = row.querySelector(".vrf-rt")?.value;

        if (name || rd || rt) {
            data.push({ name, rd, rt });
        }
    });

    return data;
}

document.getElementById("generate-vrf")?.addEventListener("click", async () => {
    try {
        window.configVrf = await fetchSection("/generate/vrf", collectVrfData());
        updateConfigOutput();
    } catch (err) {
        alert(err.message);
    }
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
