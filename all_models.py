from dataclasses import dataclass
from typing import Optional, List

@dataclass
class CoreNetwork:
    hostname: str
    loopback0: str
    loopback1: str
    hub_slice: str
    city: str
    state: str
    location_type: str
    
@dataclass
class WANConfig:
    interface: str        # Gi0/0/0 or Gi0/0/1
    provider: str 
    circuit_id: str
    ip_address: str
    bandwidth: int        # kbps
    media_type: str       # fiber, copper      

@dataclass
class RouterWANs:
    wans: List[WANConfig]
    
from dataclasses import dataclass
from typing import Optional

@dataclass
class VRFConfig:
    network: str                # sub, gas, ami, etc.
    default_gateway: str
    subnetmask: Optional[str]   # Only used for "sub" VRF
    
@dataclass
class PortConfig:
    interface: str              # Gi0/1/0 - Gi0/1/11
    description: str
    switchport_mode: str        # "access" or "trunk"
    vlan: int                   # full VLAN line or empty string
    media_type: str             # full media-type line or empty string
    shutdown: str               # "shut" or "no shut"
