# Network configuration Generator


# Config file template

```json
[
   {
      "name": "nebula-201",
      "vlans": [
         {
            "name": "11",
            "device": "bond2"
         },
         {
            "name": "516",
            "device": "bond2"
         },
         {
            "name": "576",
            "device": "bond2"
         },
         {
            "name": "999",
            "device": "bond2"
         },
         {
            "name": "1105",
            "device": "bond2"
         }
      ],
      "bridges": [
         {
            "name": "brceph",
            "device": "bond2"
         },
         {
            "name": "br-lxc",
            "device": "eth0",
            "network_config": {
               "address": "192.168.100.201",
               "netmask": "255.255.254.0",
               "gateway": "192.168.1.1"
            }
         }
      ]
   }
]
```

Or Yaml

```yaml
---
- name: nebula-201
  vlans:
  - name: 11
    device: bond2
  - name: 516
    device: bond2
  - name: 576
    device: bond2
  - name: 999
    device: bond2
  - name: 1105
    device: bond2
  bridges:
  - name: brceph
    device: bond2
  - name: br-lxc
    device: eth0
    network_config:
      address: 192.168.100.201
      netmask: 255.255.254.0
      gateway: 192.168.1.1
```