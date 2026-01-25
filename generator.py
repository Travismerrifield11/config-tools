from jinja2 import Environment, FileSystemLoader
from all_models import CoreNetwork, WANConfig, VRFConfig, PortConfig

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
    """
    Generates the Core Network configuration (hostname, loopbacks, etc.)
    """
    template = env.get_template("ir8340_core.j2")
    return template.render(core=core)


# =========================
# WAN Generator
# =========================
def generate_wan_config(core: CoreNetwork, wan: WANConfig) -> str:
    """
    Generates WAN configuration based on provider
    """
    if wan.provider.lower() == "aureon":
        template = env.get_template("WANs/aureon.j2")
    elif wan.provider.lower() == "centurylink":
        template = env.get_template("WANs/centurylink.j2")
    elif wan.provider.lower() == "charter":
        template = env.get_template("WANs/charter.j2")
    elif wan.provider.lower() == "north":
        template = env.get_template("WANs/north.j2")        
    elif wan.provider.lower() == "east":
        template = env.get_template("WANs/east.j2")        
    elif wan.provider.lower() == "south":
        template = env.get_template("WANs/south.j2")
    elif wan.provider.lower() == "west":
        template = env.get_template("WANs/west.j2")     
    elif wan.provider.lower() == "central":
        template = env.get_template("WANs/central.j2")    
    elif wan.provider.lower() == "local":
        template = env.get_template("WANs/local.j2")                
    else:
        raise ValueError(f"Unsupported WAN provider: {wan.provider}")

    return template.render(core=core, wan=wan)
    
    
# =========================
# VRF Generator
# =========================

def generate_vrf_config(core: CoreNetwork, vrf: VRFConfig):
    """
    Generates VRF configuration.
    """
    network_name = vrf.network.lower()

    if network_name == "2wr":
        template = env.get_template("VRFs/2WR.j2")
    elif network_name == "ami":
        template = env.get_template("VRFs/ami.j2")
    elif network_name == "fwbb":
        template = env.get_template("VRFs/fwbb.j2")
    elif network_name == "gas":
        template = env.get_template("VRFs/gas.j2")
    elif network_name == "ipcam":
        template = env.get_template("VRFs/ipcam.j2")
    elif network_name == "mgmt":
        template = env.get_template("VRFs/mgmt.j2")
    elif network_name == "peer":
        template = env.get_template("VRFs/peer.j2")
    elif network_name == "security":
        template = env.get_template("VRFs/physec.j2")
    elif network_name == "sub":
        template = env.get_template("VRFs/sub.j2")
    else:
        raise ValueError(f"Unsupported VRF network type: {vrf.network}")

    return template.render(core=core, vrf=vrf)


# =========================
# Port Generator
# =========================
def generate_port_config(port: PortConfig) -> str:
    """
    Generates switch port configuration.
    """
    template = env.get_template("ir8340_ports.j2")
    return template.render(port=port)

# =========================
# Full Configuration Generator
# =========================


