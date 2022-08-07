# Common Commands

Get the control plane and add-ons endpoints
`kubectl cluster-info`

Get all the nodes in the cluster
`kubectl get nodes`

Get extra details about the nodes, including  internal IP
`kubectl get nodes -o wide`

# Get all the configuration details about the node, including the allocated pod CIDR