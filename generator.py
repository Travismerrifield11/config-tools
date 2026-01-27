// generator.js
from jinja2 import Environment, FileSystemLoader
import { renderIr8340Core } from "./templates/ir8340_core.js";


env = Environment(loader=FileSystemLoader("templates"))
template = env.get_template("ir8340_core.j2")

def generate_core_config(data):
    return template.render(**data)

def generate_wan_config(data):
    """
    data: list of dicts with keys circuit, ip, bandwidth, media_type
    Returns a string of WAN configs
    """
    config_lines = ["! WAN Configuration"]
    for wan in data:
        circuit = wan.get("circuit","")
        ip = wan.get("ip","")
        bandwidth = wan.get("bandwidth","")
        media = wan.get("media_type","")
        config_lines.append(f"interface {circuit}")
        if ip:
            config_lines.append(f" ip address {ip} 255.255.255.0")
        if bandwidth:
            config_lines.append(f" bandwidth {bandwidth}")
        if media:
            config_lines.append(f" media-type {media}")
        config_lines.append("!")
    return "\n".join(config_lines)
	
def generate_vrf_config(data):
    """
    data: list of dicts with keys name, rd, rt
    Returns string of VRF configs
    """
    config_lines = ["! VRF Configuration"]
    for vrf in data:
        name = vrf.get("name","")
        rd = vrf.get("rd","")
        rt = vrf.get("rt","")
        if name:
            config_lines.append(f"vrf {name}")
            if rd:
                config_lines.append(f" rd {rd}")
            if rt:
                config_lines.append(f" route-target export {rt}")
                config_lines.append(f" route-target import {rt}")
            config_lines.append("!")
    return "\n".join(config_lines)

def generate_ports_config(data):
    """
    data: list of dicts with keys interface, ip, description, media_type
    """
    config_lines = ["! Ports Configuration"]
    for port in data:
        intf = port.get("interface","")
        ip = port.get("ip","")
        desc = port.get("description","")
        media = port.get("media_type","")
        if intf:
            config_lines.append(f"interface {intf}")
            if ip:
                config_lines.append(f" ip address {ip} 255.255.255.0")
            if desc:
                config_lines.append(f" description {desc}")
            if media:
                config_lines.append(f" media-type {media}")
            config_lines.append("!")
    return "\n".join(config_lines)


export function generateCoreConfig(coreData) {
    return renderIr8340Core(coreData);
}
