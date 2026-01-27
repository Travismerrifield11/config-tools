from jinja2 import Environment, FileSystemLoader
from lib.all_models import CoreNetwork, WANConfig, VRFConfig, PortConfig

# Initialize Jinja2 environment
env = Environment(
    loader=FileSystemLoader("templates"),
    trim_blocks=True,
    lstrip_blocks=True
)

# =========================
# Core Network Generator
# =========================
def generate_core_config(core: CoreNetwork) -> str:
    template = env.get_template("ir8340_core.j2")
    return template.render(core=core)


# =========================
# WAN Section Generator (list)
# =========================
def generate_wan_config(wans: list[WANConfig]) -> str:
    section_text = ""
    for wan in wans:
        provider = wan.provider.lower()
        # dynamic template selection based on provider
        try:
            template = env.get_template(f"WANs/{provider}.j2")
        except Exception:
            raise ValueError(f"No template for WAN provider '{wan.provider}'")
        section_text += template.render(wan=wan) + "\n"
    return section_text.strip()


# =========================
# VRF Section Generator (list)
# =========================
def generate_vrf_config(vrfs: list[VRFConfig]) -> str:
    section_text = ""
    for vrf in vrfs:
        network_name = vrf.network.lower()
        # pick the VRF template
        try:
            template = env.get_template(f"VRFs/{network_name}.j2")
        except Exception:
            raise ValueError(f"No template for VRF '{vrf.network}'")
        section_text += template.render(vrf=vrf) + "\n"
    return section_text.strip()


# =========================
# Ports Section Generator (list)
# =========================
def generate_ports_config(ports: list[PortConfig]) -> str:
    section_text = ""
    template = env.get_template("ir8340_ports.j2")
    for port in ports:
        section_text += template.render(port=port) + "\n"
    return section_text.strip()
