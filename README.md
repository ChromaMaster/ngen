# Network configuration Generator


# Config file template

```json
[
   {
      "name": "server-1",
      "vlans": [
         {
            "name": "18",
            "device": "bond2"
         },
         {
            "name": "888",
            "device": "eth0"
         },
      ],
      "bridges": [
         {
            "name": "br-kvm",
            "device": "bond2"
         },
         {
            "name": "br-lxc",
            "device": "eth0",
            "network_config": {
               "address": "192.168.1.254",
               "netmask": "255.255.255.0",
               "gateway": "192.168.1.1"
            }
         }
      ]
   }
]
```