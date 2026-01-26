// ===================== CONFIG AREA SCRIPT =====================

// --------------------- Memory Storage ---------------------
window.configCore = "";
window.configWan = "";
window.configVrf = "";
window.configPorts = "";

// --------------------- Update Textarea ---------------------
function updateConfigOutput() {
    let combined = "";
    if (document.getElementById("toggle-core")?.checked) combined += window.configCore + "\n";
    if (document.getElementById("toggle-wan")?.checked) combined += window.configWan + "\n";
    if (document.getElementById("toggle-vrf")?.checked) combined += window.configVrf + "\n";
    if (document.getElementById("toggle-ports")?.checked) combined += window.configPorts + "\n";

    document.getElementById("config-output").value = combined.trim();
}

// --------------------- Listen for Section Toggle Changes ---------------------
["toggle-core", "toggle-wan", "toggle-vrf", "toggle-ports"].forEach(id => {
    const checkbox = document.getElementById(id);
    if (checkbox) checkbox.addEventListener("change", updateConfigOutput);
});

// --------------------- Helper to POST JSON ---------------------
async function fetchSection(url, data) {
    try {
        const response = await fetch(`http://127.0.0.1:5000${url}`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(data),
        });
        if (!response.ok) throw new Error(`Failed to generate ${url}`);
        const result = await response.json();
        return result.config;  // Flask returns JSON { "config": "<text>" }
    } catch (err) {
        console.error("Fetch error:", err);
        alert(`Error generating config for ${url}: ${err.message}`);
        return "";
    }
}

// ====================== CORE GENERATE ======================
document.addEventListener("DOMContentLoaded", () => {
    const coreBtn = document.getElementById("generate-core");
    if (!coreBtn) {
        console.warn("Generate Core button not found");
        return;
    }

    coreBtn.addEventListener("click", async () => {
        const coreData = {
            hostname: document.getElementById("hostname")?.value.trim(),
            loopback0: document.getElementById("loopback0")?.value.trim(),
            loopback1: document.getElementById("loopback1")?.value.trim(),
            hub_slice: document.getElementById("hub_slice")?.value,
            city: document.getElementById("city")?.value.trim(),
            state: document.getElementById("state")?.value,
            location_type: document.getElementById("location_type")?.value,
        };

        console.log("Generating CORE config:", coreData);

        window.configCore = await fetchSection("/generate/core", coreData);
        updateConfigOutput();
    });
});

// ====================== WAN GENERATE ======================
function collectWanData() {
    const rows = document.querySelectorAll("#wan-table tbody tr");
    const data = [];

    rows.forEach(row => {
        const circuit = row.querySelector(".wan-circuit")?.value;
        const ip = row.querySelector(".wan-ip")?.value;
        const bandwidth = row.querySelector(".wan-bandwidth")?.value;

        if (circuit || ip || bandwidth) data.push({ circuit, ip, bandwidth });
    });

    return data;
}

const wanGenerateBtn = document.getElementById("generate-wan");
if (wanGenerateBtn) {
    wanGenerateBtn.addEventListener("click", async () => {
        const wanData = collectWanData();
        window.configWan = await fetchSection("/generate/wan", wanData);
        updateConfigOutput();
    });
}

// ====================== VRF GENERATE ======================
function collectVrfData() {
    const rows = document.querySelectorAll("#vrf-table tbody tr");
    const data = [];

    rows.forEach(row => {
        const name = row.querySelector(".vrf-name")?.value;
        const rd = row.querySelector(".vrf-rd")?.value;
        const rt_import = row.querySelector(".vrf-rt-import")?.value;
        const rt_export = row.querySelector(".vrf-rt-export")?.value;

        if (name || rd || rt_import || rt_export)
            data.push({ name, rd, rt_import, rt_export });
    });

    return data;
}

const vrfGenerateBtn = document.getElementById("generate-vrf");
if (vrfGenerateBtn) {
    vrfGenerateBtn.addEventListener("click", async () => {
        const vrfData = collectVrfData();
        window.configVrf = await fetchSection("/generate/vrf", vrfData);
        updateConfigOutput();
    });
}

// ====================== PORTS GENERATE ======================
function collectPortsData() {
    const rows = document.querySelectorAll("#ports-table tbody tr");
    const data = [];

    rows.forEach(row => {
        const interfaceName = row.querySelector(".port-interface")?.value;
        const ip = row.querySelector(".port-ip")?.value;
        const description = row.querySelector(".port-desc")?.value;
        const mediaType = row.querySelector(".port-media")?.value;

        if (interfaceName || ip || description || mediaType) {
            data.push({
                interface: interfaceName,
                ip,
                description,
                media_type: mediaType
            });
        }
    });

    return data;
}

const portsGenerateBtn = document.getElementById("generate-ports");
if (portsGenerateBtn) {
    portsGenerateBtn.addEventListener("click", async () => {
        const portsData = collectPortsData();
        window.configPorts = await fetchSection("/generate/ports", portsData);
        updateConfigOutput();
    });
}
