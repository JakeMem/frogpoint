ANSIBLE_FLAGS=

local:
	@ vagrant up
	@ ansible-playbook playbook.yml -l local $(ANSIBLE_FLAGS)

tarf:
	@ ansible-playbook playbook.yml -l tarf --ask-sudo-pass $(ANSIBLE_FLAGS)

.PHONY: local tarf
