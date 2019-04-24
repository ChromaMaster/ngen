import os
import sys
import json
import yaml


def fetch_interfaces(server_name, interfaces):
    for interface in interfaces:    
        pass


def fetch_vlans(server_name, vlans):
    for vlan in vlans:
        filename = "{}/vlan{}".format(server_name, vlan["name"])
        with(open(filename, "w")) as f:
            text = (
                "auto {device}.{name}\n" +
                "iface {device}.{name} inet manual\n"
                "\tvlan-raw-device {device}"
            ).format(**vlan)

            f.write(text)


def fetch_bridges(server_name, bridges):
    for bridge in bridges:
        bridge_name = bridge["name"]
        filename = "{}/{}".format(server_name, bridge_name)

        bridge_mode = "manual"
        orphan_bridge = False

        if("device" not in bridge):
            orphan_bridge = True

        # If th bridge has IP address it will be set as static config
        if("network_config" in bridge):
            bridge_mode = "static"
            netconfig = bridge["network_config"]

        with(open(filename, "w")) as f:
            text = "auto {}\n".format(bridge_name)
            text += "iface {} inet {}\n".format(bridge_name, bridge_mode)

            # Add the bridge IP config
            if(bridge_mode == "static"):
                text += "#Bridge address\n"
                for key, value in netconfig.items():
                    text += "\t{} {}\n".format(key,value)

            # if(not orphan_bridge):
            text += (
                "\n#Bridge parameters\n"
                "\tbridge_ports {device}\n" +
                "\tbidge_stp off\n" +
                "\tbridge_fd 0\n" +
                "\tbridge_maxwait 0\n"
            ).format(**bridge)

            # Add interface hooks
            if("hooks" in bridge):
                text += "\n#Hooks\n"
                allowed_hooks = ["pre-up", "up", "post-up", "pre-down", "down", "post-down"]
                for key, value in bridge["hooks"].items():                
                    if(key not in allowed_hooks):
                        print("Warning: hook {} ({}.{}) not defined".format(key, server_name, bridge_name))
                        continue
                    text += (
                        "\t{} {}\n".format(key, value)
                    )
            f.write(text)

def main(data_path, file_type):

    with(open(data_path, "r")) as f:
        if(file_type == "json"):
            data = json.load(f)
        else:
            data = yaml.load(f, yaml.SafeLoader)

    for machine in data:
        server_name = machine["name"]

        # Creates a directory to store network config files
        if(not os.path.exists(server_name)):
            os.mkdir(server_name)

        # Look for interfaces
        # TODO:
        # fetch_interfaces(server_name, machine["interfaces"])

        # Look for vlans
        fetch_vlans(server_name, machine["vlans"])

        # Look for bridges
        fetch_bridges(server_name, machine["bridges"])

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Usage {} data_file".format(sys.argv[0]))
        sys.exit()

    available_extensions = ["json", "yaml", "yml"]

    # Gets the extension and remove the dot (eg. .json -> json)
    extension = os.path.splitext(sys.argv[1])[1]
    extension = extension[1:]

    if extension not in available_extensions:
        print("Error: data file format, must be <{}>".format(available_extensions))
        sys.exit()

    main(sys.argv[1], extension)
