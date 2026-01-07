import tkinter as tk
import re
import ipaddress
import tkinter.messagebox as messagebox
import os
from tkinter import ttk, filedialog, Text

"""
=======================
Version 3.0 
=======================
(12/12/2024)
Bug Fixes
-Changed the order of # Switch Port Config Find and Replace loop so gi1 doesnt replace gi10 toggles.

"""

class RouterConfigApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Router Configuration Tool")

        # Set default window size
        self.geometry("700x950")  # Set the width and height as desired

        # Create a canvas to contain all frames
        canvas = tk.Canvas(self)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Add a scrollbar
        scrollbar = ttk.Scrollbar(self, orient=tk.VERTICAL, command=canvas.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a frame to contain all sections
        container = ttk.Frame(canvas)
        container.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        # Configure canvas scrolling
        canvas.create_window((0, 0), window=container, anchor=tk.NW)
        canvas.configure(yscrollcommand=scrollbar.set)
        canvas.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        scrollbar.config(command=canvas.yview)

        # Basic Configuration Section
        basic_frame = ttk.LabelFrame(container, text="Basic Configuration")
        basic_frame.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        # Select WAN Section
        wan_frame = ttk.LabelFrame(container, text="Select WAN")
        wan_frame.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # Select Networks Section
        networks_frame = ttk.LabelFrame(container, text="Select Networks")
        networks_frame.grid(row=2, column=0, padx=10, pady=5, sticky="w")

        # Switch Port Setup Section
        port_frame = ttk.LabelFrame(container, text="Switch Port Setup")
        port_frame.grid(row=3, column=0, padx=10, pady=5, sticky="w")

        # Create a frame at the bottom of the container
        bottom_frame = ttk.Frame(container)
        bottom_frame.grid(row=4, column=0, pady=10)

        # Update canvas scrolling region
        container.update_idletasks()  # Update container to get accurate size
        canvas.config(scrollregion=canvas.bbox("all"))

        # Basic Config Section
        ttk.Label(basic_frame, text="Hostname:").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.hostname_entry = ttk.Entry(basic_frame)
        self.hostname_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(basic_frame, text="Loopback 0 IP:").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.loopback0_ip_entry = ttk.Entry(basic_frame)
        self.loopback0_ip_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(basic_frame, text="Loopback 1 IP:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
        self.loopback1_ip_entry = ttk.Entry(basic_frame)
        self.loopback1_ip_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        tk.Label(basic_frame, text="Hub Splice:").grid(row=3, column=0, padx=5, pady=5, sticky="w")
        hub_options = ["07", "08", "09", "10", "11", "12"]
        self.hub_dropdown = ttk.Combobox(basic_frame, values=hub_options, state="readonly")
        self.hub_dropdown.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(basic_frame, text="City:").grid(row=0, column=3, padx=5, pady=5, sticky="e")
        self.city_entry = ttk.Entry(basic_frame)
        self.city_entry.grid(row=0, column=4, padx=5, pady=5, sticky="w")

        ttk.Label(basic_frame, text="State:").grid(row=1, column=3, padx=5, pady=5, sticky="e")
        state_options = ["IA", "IL", "MN", "WI"]
        self.state_dropdown = ttk.Combobox(basic_frame, values=state_options, state="readonly")
        self.state_dropdown.grid(row=1, column=4, padx=5, pady=5, sticky="w")

        ttk.Label(basic_frame, text="Location Type:").grid(row=2, column=3, padx=5, pady=5, sticky="e")
        location_type_options = ["Gen", "Ops", "Sub", "Tower", "Gas"]
        self.location_type_dropdown = ttk.Combobox(basic_frame, values=location_type_options, state="readonly")
        self.location_type_dropdown.grid(row=2, column=4, padx=4, pady=4, sticky="w")

        # Networks Section

        self.network_vars = {}
        self.network_entries = {}
        self.selected_networks = set()  # Set to store selected networks
        networks = ["2WR", "AMI", "FWBB", "GAS", "IPCAM", "MGMT", "Peer", "SEC", "SUB"]
        for i, network in enumerate(networks):
            var = tk.BooleanVar(value=False)
            var.trace_add("write",
                          lambda *args, network=network: self.toggle_network_fields(network))
            self.network_vars[network] = var
            checkbox = ttk.Checkbutton(networks_frame, text=network, variable=var)
            checkbox.grid(row=i + 1, column=0, padx=5, pady=2, sticky="w")

            # Default Gateway Entry Fields
            self.network_entries[network] = {}
            self.network_entries[network]['ip'] = ttk.Entry(networks_frame, state='disabled')
            self.network_entries[network]['ip'].grid(row=i + 1, column=1, padx=5, pady=2, sticky="w")

            # Subnet mask labels or dropdown for SUB network
            if network == "SUB":
                self.subnet_var = tk.StringVar(value="Select Subnet")
                self.subnet_dropdown = ttk.Combobox(networks_frame, textvariable=self.subnet_var, state="disabled")

                self.subnet_dropdown['values'] = [
                    "255.255.255.248",
                    "255.255.255.240",
                    "255.255.255.192"
                ]
                self.subnet_dropdown.grid(row=i + 1, column=2, padx=5, pady=2, sticky="w")
                # self.subnet_dropdown.grid_remove()
            else:
                subnet_mask_text = {
                    "2WR": "255.255.255.240",
                    "AMI": "255.255.255.240",
                    "FWBB": "255.255.255.240",
                    "GAS": "255.255.255.248",
                    "IPCAM": "255.255.255.240",
                    "MGMT": "255.255.255.240",
                    "Peer": "255.255.255.248",
                    "SEC": "255.255.255.240",
                }
                ttk.Label(networks_frame, text=subnet_mask_text[network]).grid(row=i + 1, column=2, padx=5, pady=2,
                                                                               sticky="s")

        ttk.Label(networks_frame, text="Default Gateway").grid(row=0, column=1, padx=5, pady=2, sticky="s")
        ttk.Label(networks_frame, text="Subnet Mask").grid(row=0, column=2, padx=5, pady=2, sticky="s")

        # Update dropdown visibility based on SUB checkbox
        self.network_vars["SUB"].trace_add("write", self.toggle_dropdown)

        # WAN Section

        self.wan_vars = {}
        self.wan_entries = {}
        self.selected_wan = set()  # Set to store selected networks
        wans = ["Aureon", "CenturyLink", "Charter", "North", "East", "South", "West", "Central", "Local"]
        service_options = ["RJ45", "SFP"]

        # Define interface names and loop over them to set up rows
        interfaces = ["gi 0/0/0", "gi 0/0/1"]
        for row, interface_name in enumerate(interfaces, start=1):
            # Checkbox for the interface
            var = tk.BooleanVar(value=False)
            var.trace_add("write", lambda *args, iface=interface_name: self.toggle_wan_fields(iface))
            self.wan_vars[interface_name] = var

            checkbox = ttk.Checkbutton(wan_frame, text=interface_name, variable=var)
            checkbox.grid(row=row, column=0, padx=5, pady=2, sticky="w")

            # Dropdown for selecting WAN
            wan_dropdown = ttk.Combobox(wan_frame, values=wans, state="disabled", width=15)
            wan_dropdown.grid(row=row, column=1, padx=5, pady=2, sticky="w")

            # WAN Circuit ID
            wan_circuit = ttk.Entry(wan_frame, state='disabled')
            wan_circuit.grid(row=row, column=2, padx=5, pady=2, sticky="w")

            # WAN IP Entry field
            wan_ip_entry = ttk.Entry(wan_frame, state='disabled')
            wan_ip_entry.grid(row=row, column=3, padx=5, pady=2, sticky="w")

            # WAN Bandwidth
            wan_bandwidth = ttk.Entry(wan_frame, state='disabled',width=15)
            wan_bandwidth.grid(row=row, column=4, padx=5, pady=2, sticky="w")

            # Media Type Dropdown
            media_type_dropdown = ttk.Combobox(wan_frame, values=service_options, state='disabled', width=7)
            media_type_dropdown.grid(row=row, column=5, padx=5, pady=2, sticky="w")

            # Store entry widgets in wan_entries for later access
            self.wan_entries[interface_name] = {
                "wan_dropdown": wan_dropdown,
                "ip": wan_ip_entry,
                "Media Type": media_type_dropdown,
                "circuit": wan_circuit,
                "bandwidth": wan_bandwidth
            }

        # Labels for wan section
        ttk.Label(wan_frame, text="WAN").grid(row=0, column=1, padx=5, pady=2, sticky="s")
        ttk.Label(wan_frame, text="Circuit ID").grid(row=0, column=2, padx=5, pady=2, sticky="s")
        ttk.Label(wan_frame, text="WAN IP").grid(row=0, column=3, padx=5, pady=2, sticky="s")
        ttk.Label(wan_frame, text="Bandwidth (kbps)").grid(row=0, column=4, padx=5, pady=2, sticky="s")
        ttk.Label(wan_frame, text="Media Type").grid(row=0, column=5, padx=5, pady=2, sticky="s")


        # Port Section

        self.port_vars = {}
        self.port_entries = {}
        self.port_network_dropdowns = {}
        self.port_service_dropdowns = {}

        ports = ["GI - 0/1/0", "GI - 0/1/1", "GI - 0/1/2", "GI - 0/1/3", "GI - 0/1/4", "GI - 0/1/5",
                 "GI - 0/1/6", "GI - 0/1/7", "GI - 0/1/8", "GI - 0/1/9", "GI - 0/1/10", "GI - 0/1/11"]

        for i, port in enumerate(ports):
            var = tk.BooleanVar(value=False)
            self.port_vars[port] = var
            ttk.Checkbutton(port_frame, text=port, variable=var,
                            command=lambda p=port: self.toggle_port_fields(p)).grid(row=i + 1, column=0, padx=5, pady=2,
                                                                                    sticky="w")

            # Create entry for description
            self.port_entries[port] = {}
            self.port_entries[port]["Description"] = ttk.Entry(port_frame, state='disabled')
            self.port_entries[port]["Description"].grid(row=i + 1, column=1, padx=5, pady=2, sticky="w")

            # Create dropdown for network
            network_options = ttk.Combobox(port_frame, state='disabled')
            network_options.grid(row=i + 1, column=2, padx=5, pady=2, sticky="w")
            self.port_network_dropdowns[port] = network_options

            # Create dropdown for Media Type for rows 5-8
            if 4 <= i < 8:
                service_options = ["RJ45", "SFP"]
                self.port_entries[port]["Media Type"] = ttk.Combobox(port_frame, values=service_options,
                                                                     state='disabled', width=7)
                self.port_entries[port]["Media Type"].grid(row=i + 1, column=3, padx=5, pady=2, sticky="w")

        # Labels for Description, Network, and Media Type
        ttk.Label(port_frame, text="Description").grid(row=0, column=1, padx=5, pady=2, sticky="s")
        ttk.Label(port_frame, text="Network").grid(row=0, column=2, padx=5, pady=2, sticky="s")
        ttk.Label(port_frame, text="Media Type").grid(row=0, column=3, padx=5, pady=2, sticky="s")

        # Save Button
        save_button = ttk.Button(bottom_frame, text="Save", command=self.save_config)
        save_button.grid(row=0, column=0, padx=10)

        # Instructions Button
        instructions_button = ttk.Button(bottom_frame, text="Instructions", command=self.display_instructions)
        instructions_button.grid(row=0, column=1, padx=10)

        # Center the bottom frame containing the buttons
        container.grid_rowconfigure(3, weight=1)
        container.grid_columnconfigure(0, weight=1)

    def toggle_dropdown(self, *args):
        if self.network_vars["SUB"].get():
            self.subnet_dropdown["state"] = "readonly"
        else:
            self.subnet_dropdown["state"] = "disabled"

    def toggle_port_fields(self, port):
        is_enabled = self.port_vars[port].get()  # True if checked, False if unchecked
        state = 'normal' if is_enabled else 'disabled'

        # Set the state of each field based on toggle button status
        self.port_entries[port]["Description"].config(state=state)
        self.port_network_dropdowns[port].config(state="readonly" if is_enabled else state)

        if port in self.port_service_dropdowns:
            self.port_service_dropdowns[port].config(state="readonly" if is_enabled else state)

        if 4 <= int(port.split('/')[-1]) < 8:
            self.port_entries[port]["Media Type"].config(state="readonly" if is_enabled else state)

        # Clear the fields when disabled
        if not is_enabled:
            self.port_entries[port]["Description"].delete(0, 'end')  # Clear plain text entry
            self.port_network_dropdowns[port].set('')  # Clear dropdown selection
            if port in self.port_service_dropdowns:
                self.port_service_dropdowns[port].set('')
            if 4 <= int(port.split('/')[-1]) < 8:
                self.port_entries[port]["Media Type"].set('')

    def toggle_network_fields(self, network):
        state = 'normal' if self.network_vars[network].get() else 'disabled'
        self.network_entries[network]['ip'].config(state=state)

        # Update port dropdowns when network checkbox is toggled
        self.update_port_dropdowns()

    def toggle_wan_fields(self, wan):
        is_enabled = self.wan_vars[wan].get()  # True if checked, False if unchecked
        state = 'normal' if is_enabled else 'disabled'

        # Set the state of each field based on toggle button status
        self.wan_entries[wan]['ip'].config(state=state)
        self.wan_entries[wan]['circuit'].config(state=state)
        self.wan_entries[wan]['bandwidth'].config(state=state)

        if wan in self.wan_entries:
            self.wan_entries[wan]["Media Type"].config(state="readonly" if is_enabled else state)
            self.wan_entries[wan]["wan_dropdown"].config(state="readonly" if is_enabled else state)

        # Clear the fields when disabled
        if not is_enabled:
            # Temporarily enable fields to clear them if necessary
            self.wan_entries[wan]['ip'].config(state='normal')
            self.wan_entries[wan]['ip'].delete(0, 'end')
            self.wan_entries[wan]['ip'].config(state=state)

            self.wan_entries[wan]['circuit'].config(state='normal')
            self.wan_entries[wan]['circuit'].delete(0, 'end')
            self.wan_entries[wan]['circuit'].config(state=state)

            self.wan_entries[wan]['bandwidth'].config(state='normal')
            self.wan_entries[wan]['bandwidth'].delete(0, 'end')
            self.wan_entries[wan]['bandwidth'].config(state=state)

            # Clear dropdown selections
            self.wan_entries[wan]["Media Type"].set('')  # Clear dropdown
            self.wan_entries[wan]["wan_dropdown"].set('')  # Clear dropdown

    def update_port_dropdowns(self):
        available_networks = [net for net, var in self.network_vars.items() if var.get()]

        for port, dropdown in self.port_network_dropdowns.items():
            dropdown.config(values=available_networks)

            # Retrieve the current selection of the dropdown and reset it if it's not available
            current_selection = dropdown.get()
            if current_selection not in available_networks:
                dropdown.set('')  # Reset to empty if the current selection is not available

    def display_instructions(self):
        # Create a new window to display instructions
        instructions_window = tk.Toplevel(self)
        instructions_window.title("Instructions")

        # Load the contents of the instruction file
        with open("IR8340 config tool instructions.txt", "r") as file:
            instructions_text = file.read()

        # Create a label to display the instructions with dynamic wrapping
        instructions_text_widget = Text(instructions_window, wrap="word")
        instructions_text_widget.insert("1.0", instructions_text)
        instructions_text_widget.config(state="disabled")  # Disable editing
        instructions_text_widget.pack(expand=True, fill="both")

        # Close Button
        ttk.Button(instructions_window, text="Close", command=instructions_window.destroy).pack(pady=10)

    def validate_ip(self, ip: str, label: str, invalid_ips: list) -> bool:
        """
        Validates a given IP address and appends any invalid IP details to the invalid_ips list.
        """
        try:
            ipaddress.ip_address(ip)
            return True
        except ValueError:
            invalid_ips.append(f"{label}: {ip}")
            return False
    def save_config(self):
        # Get user inputs
        invalid_ips = []  # Initialize invalid IPs list
        hostname = self.hostname_entry.get()
        loopback0 = self.loopback0_ip_entry.get()
        loopback1 = self.loopback1_ip_entry.get()
        hub = self.hub_dropdown.get()
        city = self.city_entry.get()
        state = self.state_dropdown.get()
        location_type = self.location_type_dropdown.get()
        port_network_numbers = {}
        port_mediatypes = {}

        self.validate_ip(loopback0, "Loopback0", invalid_ips)
        self.validate_ip(loopback1, "Loopback1", invalid_ips)

        # Mapping of networks to numbers
        network_numbers = {
            "2WR": "50",
            "AMI": "53",
            "FWBB": "56",
            "GAS": "54",
            "IPCAM": "58",
            "MGMT": "30",
            "Peer": "67",
            "SEC": "59",
            "SUB": "51"
        }


        # Read the contents of the text file
        file_path = "IR8340 config tool template 3.0.txt"
        with open(file_path, 'r') as file:
            file_content = file.read()

        # Basic Config Find and Replace
        file_content = file_content.replace("insert-hostname", hostname)
        file_content = file_content.replace("insert-loopback0", loopback0)
        file_content = file_content.replace("insert-loopback1", loopback1)
        file_content = file_content.replace("insert-hubsplice", hub)
        file_content = file_content.replace("insert-city", city)
        file_content = file_content.replace("insert-state", state)
        file_content = file_content.replace("insert-location_type", location_type)

        # Select VRF's To Find and Replace
        for network, var in self.network_vars.items():
            if var.get():
                file_content = file_content.replace(f"!toggle-{network.lower()}", "")
                gateway = self.network_entries[network]["ip"].get()
                self.validate_ip(gateway, network, invalid_ips)
                file_content = file_content.replace(f"insert-{network.lower()}-gateway", gateway)
                if network == "SUB":
                    selected_subnet = self.subnet_dropdown.get()
                    file_content = file_content.replace("insert-sub-subnet", selected_subnet)
                    print(selected_subnet)
            else:
                file_content = re.sub(fr"^.*!toggle-{network.lower()}.*$", "", file_content, flags=re.MULTILINE)


        # WAN Port Config Find and Replace
        interfaces = ["gi 0/0/0", "gi 0/0/1"]
        used_toggles = set()
        # First Pass: Collect toggles and handle WAN-specific replacements
        for wan_port_name in interfaces:
            wan_dropdown = self.wan_entries[wan_port_name]["wan_dropdown"].get()
            wan_ip = self.wan_entries[wan_port_name]["ip"].get()
            wan_media_type = self.wan_entries[wan_port_name]["Media Type"].get()
            wan_circuit = self.wan_entries[wan_port_name]["circuit"].get()
            wan_bandwidth = self.wan_entries[wan_port_name]["bandwidth"].get()

            if self.wan_vars[wan_port_name].get():  # Enabled
                used_toggles.add(wan_dropdown)
                self.validate_ip(wan_ip, wan_port_name, invalid_ips)
                file_content = file_content.replace(f"insert-wan-ip", wan_ip)
                file_content = file_content.replace(f"insert-wan-port", wan_port_name)
                file_content = file_content.replace(f"insert-wan-media", wan_media_type)
                file_content = file_content.replace(f"gi0/0/0-shut", "no shutdown")
                file_content = file_content.replace(f"insert-circuit-id", wan_circuit)
                file_content = file_content.replace(f"insert-bandwidth", wan_bandwidth)
            else:  # Disabled
                file_content = file_content.replace(f"!{wan_port_name}-shut", "shutdown")

        # Second Pass: Process toggles in the file
        lines = file_content.splitlines()
        processed_lines = []

        # Process WAN-specific toggles in the file
        lines = file_content.splitlines()
        processed_lines = []

        for line in lines:
            stripped_line = line.lstrip()  # Remove leading spaces or tabs for processing
            if stripped_line.startswith("!toggle-wan"):  # Process only WAN-specific toggles
                # Extract the toggle keyword after "!toggle-wan-" (e.g., "local")
                toggle_keyword = stripped_line.split(" ", 1)[0][12:]
                if toggle_keyword in used_toggles:
                    # Add only the value (e.g., "local") to the output
                    processed_lines.append(stripped_line.split(" ", 1)[1])
                # Else: exclude this line entirely (disabled toggle)
            else:
                # Preserve non-WAN toggle lines and other content
                processed_lines.append(line)

        file_content = "\n".join(processed_lines)

        # Switch Port Config Find and Replace
        for i in range(11, -1, -1):
            port_name = f"GI - 0/1/{i}"
            port_desc = self.port_entries[port_name]["Description"].get()
            port_network = self.port_network_dropdowns[port_name].get()
            port_network_number = network_numbers.get(port_network, "")
            port_network_numbers[port_name] = port_network_number

            # Conditionally add media type for ports 4 through 7
            if 4 <= i <= 7:
                port_mediatypes[port_name] = self.port_entries[port_name]["Media Type"].get()
                file_content = file_content.replace(f"!gi{i}-mediatype", port_mediatypes[port_name])

            if self.port_vars[port_name].get():
                # Handle toggling and other replacements
                file_content = file_content.replace(f"!toggle-gi{i}", "")  # Only replace the toggle marker
                file_content = file_content.replace(f"insert-gi{i}-desc", port_desc)
                file_content = file_content.replace(f"!gi{i}-shut", "no shutdown")
                file_content = file_content.replace(f"!gi{i}-network", port_network_number)
            else:
                # Handle toggling and other replacements
                file_content = re.sub(fr"^.*!toggle-gi{i}\b.*$", "", file_content, flags=re.MULTILINE)
                file_content = file_content.replace(f"!gi{i}-shut", "shutdown")

                # If any IPs are invalid, show an error
        if invalid_ips:
            messagebox.showerror("Invalid IP Addresses",
                                f"The following IP addresses are invalid:\n" + "\n".join(invalid_ips))
            return

        # Remove consecutive blank lines
        file_content = re.sub(r"\n\s*\n+", "\n", file_content)  # Remove consecutive blank lines

        # Write the modified content to a new file
        file_path = filedialog.asksaveasfilename(
            initialdir=os.path.expanduser("~/Desktop"),  # Start in the user's desktop
            defaultextension=".txt",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
        )
        if file_path:
            # Write the modified content to the selected file path
            with open(file_path, 'w') as new_file:
                new_file.write(file_content)


            print(f"Find and replace operation completed. File saved as '{file_path}'")
            os.startfile(file_path)


if __name__ == "__main__":
    app = RouterConfigApp()
    app.mainloop()
