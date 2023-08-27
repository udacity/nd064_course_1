## ArgoCD Manifests 

Place the ArgoCD manifests in this directory.


```
# To retrieve the initial password for ArgoCD, you can use the following command:
sudo k3s kubectl --namespace argocd get secret argocd-initial-admin-secret -o json | jq -r '.data.password' | base64 -d
```