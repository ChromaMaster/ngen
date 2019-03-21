import os
import sys
import json

def main(data_path):
    with(open(data_path, "r")) as f:
        data = json.load(f)
    
    for machine in data:
        dirpath = machine["name"]

        # Creates a directory to store network config files
        if(not os.path.exists(dirpath)):
            os.mkdir(dirpath)

        # Look for vlans
        for vlan in machine["vlans"]:
            filename = "{}/vlan{}".format(dirpath, vlan["name"])
            with(open(filename, "w")) as f:
                text =(
                    "auto {device}.{name}\n" + 
                    "iface {device}.{name} int manual"                    
                ).format(**vlan)                
                f.write(text)

        # Look for bridges
        for bridge in machine["bridges"]:
            filename = "{}/{}".format(dirpath, bridge["name"])
            bridge_mode = "manual"

            # If th bridge has IP address it will be set as static config
            if("network_config" in bridge):
                bridge_mode = "static"
                netconfig = bridge["network_config"]
        
            with(open(filename, "w")) as f:            
                text  = "auto {}\n".format(bridge["name"])
                text += "iface {} inet {}\n".format(bridge["name"], bridge_mode)
                
                # Add the bridge IP config
                if(bridge_mode == "static"):
                    text += (
                        "\taddress {address}\n" + 
                        "\tnetmask {netmask}\n" +
                        "\tgatseway {gateway}\n"
                    ).format(**netconfig)
                    
                text += (
                    "\tbridge_ports {device}\n" +
                    "\tbidge_stp off\n" +
                    "\tbridge_fd 0\n" +
                    "\tbridge_maxwait 0\n"
                ).format(**bridge)

                f.write(text)

if __name__ == "__main__":
    if (len(sys.argv) < 2):
        print("Usage {} data".format(sys.argv[0]))
        sys.exit();

    main(sys.argv[1])

