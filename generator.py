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
# VRF Section Generator
# =========================
def generate_vrf_config(core, vrf, template_name):
    env = Environment(loader=FileSystemLoader("Templates"))  # base folder
    template = env.get_template(f"IPL/VRFs/{template_name}")   # relative path inside Templates
    return template.render(core=core, vrf=vrf)


# =========================
# Ports Section Generator (list)
# =========================
def generate_ports_config(ports: list[PortConfig]) -> str:
    section_text = ""
    template = env.get_template("ir8340_ports.j2")
    for port in ports:
        section_text += template.render(port=port) + "\n"
    return section_text.strip()
