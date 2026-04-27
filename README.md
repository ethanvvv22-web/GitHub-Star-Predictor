## Infrastructure Contextualization
The infrastructure folder is used to contextualize the VMs and the Kubnernetes cluster using cloud init and ansible playbook.

The ansible playbook only installs the kubernetes component such as kubedm, kubelet and kubectl on all VMs. The cluster need to be manually created following the instruction here and use the command `kubeadm init --config=infrastructure/k8s-workload/kubeadm-init.yaml`: https://kubernetes.io/docs/setup/production-environment/tools/kubeadm/create-cluster-kubeadm/

## Kubernetes deployment

The cri socket for kuberadm config is changed to dockerd from the default template. When using kubeadm to join a node to the kubernetes cluster, the command must also specify the cri socket as `--cri-socket unix:///var/run/cri-dockerd.sock`.

After creating the Kubernetes cluster, the order to deploy plugins and applications are: flannel -> metrics server -> kubernetes dashboard -> dashboard svc and serviceaccount

**flannel**: The CNI for the kubernetes cluster can be installed following the instruction here: https://github.com/flannel-io/flannel Some node might need `modprobe br_netfilter` to enable flannel pod on them. There is also the possibility of encountering the problem described in this github issue: https://github.com/flannel-io/flannel/issues/728

**Monitoring**: metrics-server and kubernetes dashboard are used. Here are their respective repo:

https://github.com/kubernetes-sigs/metrics-server

https://github.com/kubernetes/dashboard

The metrics server yaml only has one change compare to the default one: `kubelet-preferred-address-types=InternalIP`

After kubernetes dashboard is deployed, a service account and a service of nodeport type must be created to access the dashboard from the public internet.

Nginx ingress controller is deployed following the instructions here: https://kubernetes.github.io/ingress-nginx/deploy/#bare-metal-clusters

## Monitoring
After kubernetes dashboard, the added service, and the service account is deployed, the dashboard can be accessed via port 30900 or 30901 of the node that pod `kubernetes-dashboard-kong` resides on. The bearer token can be obtained using this command: `kubectl get secret admin-user -n kubernetes-dashboard -o jsonpath="{.data.token}" | base64 -d`

## Model training process
Script running order: `preprocess.py` -> `train_model.py` -> `evaluate.py`
Need to compare r2_val in metadata to determine if new best model is better than old best model, only continue if it is better. **This is not automated in the github actions pipeline**
After evaluate.py is run, copy `best_model.joblib`, `scaler.joblib`, `best_model_metadata.json` to app/model for application to use

## Local dev environment test
build ml_pipeline and stargazer using the Dockerfile in their respective folder and then start docker compose.
The best model need to be manually copied to `github-star-predictor/app/model`.