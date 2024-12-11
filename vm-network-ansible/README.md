ansible-playbook -i inventory.ini -e "@variables.yaml" playbook_step_by_step.yaml

ansible-playbook -i inventory.ini -e "@variables.yaml" playbook_delete_vms.yaml

Test connection to VMs:
```
ansible all -m ping
```