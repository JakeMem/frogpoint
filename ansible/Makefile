ANSIBLE_FLAGS=

local:
	@ vagrant up
	@ ansible-playbook playbook.yml -l local $(ANSIBLE_FLAGS)

.PHONY: local
