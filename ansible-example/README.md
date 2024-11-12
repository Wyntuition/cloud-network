# Simple Ansible Playbook

Use this python env (venv with openstacksdk installed a lot python3 -m venv mypythonenv):

`source ~/mypythonenv/bin/python`

Run the playbook: 

```bash
ansible-playbook -i inventory.ini my-playbook.yaml
```

Flags

`--check` for dry run mode for debugging

`-vvv` for verbosity