# Common Commands 
Inspect available vagrant boxes 
`$ vagrant status `

Create a vagrant box using the Vagrantfile in the current directory
`$ vagrant up`

SSH into the vagrant box
`$ vagrant ssh`

copy files into the VM
`$ vagrant scp <file/dir> :<guest location>`


/Note: this command uses the .vagrant folder to identify the details of the vagrant box/

Destroy the VM
`$ vagrant destroy`

Quit the VM
`$ quit`

## Instruction for use:
1. If you haven't already, install k3s

`$ curl -sfL https://get.k3s.io | sh - `

To be able to run kubectl commands, we'll need root access (not great practice!)

`$ sudo su`

install vagrant scp!
`$ vagrant plugin install vagrant-scp`


