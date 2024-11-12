ansible-playbook -i inventory.ini -e "@variables.yaml" playbook_step_by_step.yaml

ansible-playbook -i inventory.ini -e "@variables.yaml" playbook_delete_vms.yaml

Test connection to VMs:
```
ansible all -m ping
```

## Directory structure 

ansible/
├── playbooks/
│   ├── provision_vms.yaml            # Playbook for provisioning VMs
│   └── install_kubernetes.yaml       # Playbook for installing Kubernetes
├── inventories/
│   ├── dev.ini                       # Inventory file for dev environment
│   └── prod.ini                      # Inventory file for prod environment
├── roles/
│   ├── vm_provisioning/
│   │   ├── tasks/
│   │   │   └── main.yml              # VM provisioning tasks (e.g., create VM, configure network)
│   │   └── vars/
│   │       └── main.yml              # Variables specific to VM provisioning (e.g., instance type)
│   ├── kubernetes_installation/
│   │   ├── tasks/
│   │   │   └── main.yml              # Kubernetes installation and configuration tasks
│   │   ├── vars/
│   │   │   └── main.yml              # Kubernetes-specific variables
│   │   └── templates/
│   │       └── config.yaml.j2        # Template for Kubernetes config
│   └── common/
│       ├── tasks/
│       │   └── main.yml              # Common tasks (e.g., package updates, Docker installation)
│       └── handlers/
│           └── main.yml              # Common handlers (e.g., restart services)
├── group_vars/
│   ├── all.yml                       # Global variables for all environments
│   ├── kubernetes_nodes.yml          # Group-specific variables for Kubernetes nodes
│   └── vm_hosts.yml                  # Group-specific variables for VMs
├── ansible.cfg                       # Configuration file
└── README.md                         # Documentation


