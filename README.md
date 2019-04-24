# Network configuration Generator


# Config file template

```json
[
  {
    "name": "my-server",
    "vlans": [
      {
        "name": 18,
        "device": "eth0"
      },
      {
        "name": 999,
        "device": "eth1"
      }
    ],
    "bridges": [
      {
        "name": "br-kvm",
        "device": "eth0",
        "hooks": {
          "post-up": "iptables -t nat -A POSTROUTING -o br-lxc -j SNAT --to 10.0.0.1"
        }
      },
      {
        "name": "br-lxc",
        "device": "eth0",
        "network_config": {
          "address": "192.168.1.254",
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
- name: my-server
  vlans:
  - name: 18
    device: eth0
  - name: 999
    device: eth1
  bridges:
  - name: br-kvm
    device: eth0
    hooks:
      post-up: iptables -t nat -A POSTROUTING -o br-lxc -j SNAT --to 10.0.0.1

  - name: br-lxc
    device: eth0
    network_config:
      address: 192.168.1.254
      netmask: 255.255.254.0
      gateway: 192.168.1.1
```