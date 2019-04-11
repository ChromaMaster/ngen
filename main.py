import os
import sys
import json
import yaml


def fetch_interfaces(dir_path, interfaces):
    for interface in interfaces:    
        pass


def fetch_vlans(dir_path, vlans):
    for vlan in vlans:
        filename = "{}/vlan{}".format(dir_path, vlan["name"])
        with(open(filename, "w")) as f:
            text = (
                "auto {device}.{name}\n" +
                "iface {device}.{name} inet manual"
            ).format(**vlan)

            f.write(text)


def fetch_bridges(dir_path, bridges):
    for bridge in bridges:
        filename = "{}/{}".format(dir_path, bridge["name"])

        bridge_mode = "manual"
        orphan_bridge = False

        if("device" not in bridge):
            orphan_bridge = True

        # If th bridge has IP address it will be set as static config
        if("network_config" in bridge):
            bridge_mode = "static"
            netconfig = bridge["network_config"]

        with(open(filename, "w")) as f:
            text = "auto {}\n".format(bridge["name"])
            text += "iface {} inet {}\n".format(bridge["name"], bridge_mode)

            # Add the bridge IP config
            if(bridge_mode == "static"):            
                for key, value in netconfig.items():
                    text += "\t{} {}\n".format(key,value)

            # if(not orphan_bridge):
            text += (
                "\tbridge_ports {device}\n" +
                "\tbidge_stp off\n" +
                "\tbridge_fd 0\n" +
                "\tbridge_maxwait 0\n"
            ).format(**bridge)

            f.write(text)


def main(data_path, file_type):

    with(open(data_path, "r")) as f:
        if(file_type == "json"):
            data = json.load(f)
        else:
            data = yaml.load(f, yaml.SafeLoader)

    for machine in data:
        dir_path = machine["name"]

        # Creates a directory to store network config files
        if(not os.path.exists(dir_path)):
            os.mkdir(dir_path)

        # Look for interfaces
        # TODO:
        # fetch_interfaces(dir_path, machine["interfaces"])

        # Look for vlans
        fetch_vlans(dir_path, machine["vlans"])

        # Look for bridges
        fetch_bridges(dir_path, machine["bridges"])

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
