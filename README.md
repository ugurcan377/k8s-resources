# Requirements
```
sudo apt install docker.io curl
```

# Kubernetes install
```
git clone https://github.com/Mirantis/kubeadm-dind-cluster.git  
cd kubeadm-dind-cluster  
./fixed/dind-cluster-v1.9.sh up  
```
config.sh for node count and networking  
image/kubelet.service has eviction policies. #Haven't tried it yet  

# Api server configuration
```
docker exec -it kube-master /bin/bash  
apt install vim-tiny  
vim.tiny /etc/kubeadm.conf  
```
Add following to the file  
```
apiServerExtraArgs:
  runtime-config: "api/all=true"
controllerManagerExtraArgs:
  horizontal-pod-autoscaler-use-rest-clients: "true"
  horizontal-pod-autoscaler-sync-period: "10s"
  node-monitor-grace-period: "10s"
```
Restart apiserver using kubeadm  
```
kubeadm config upload from-file --config /etc/kubeadm.conf  
kubeadm upgrade apply 1.9.1  
```

# Metrics-server install
```
git clone https://github.com/kubernetes-incubator/metrics-server.git  
cd metrics-server  
kubectl create -f deploy/1.8+/  
```

# Check metrics-server
```
kubectl api-versions  
```
Check if following api endpoints exist at the output  
```
metrics.k8s.io/v1beta1  
autoscaling/v2beta1  
```
Check if metrics-server getting any data
```
kubectl get --raw "/apis/metrics.k8s.io/v1beta1/nodes"  
kubectl get --raw "/apis/metrics.k8s.io/v1beta1/pods"  
```
# Monitoring
```
git clone https://github.com/coreos/prometheus-operator.git  
cd contrib/kube-prometheus/  
hack/cluster-monitoring/deploy  
```
Prometheus UI on node port `30900`  
Alertmanager UI on node port `30903`  
Grafana (Dashboard) on node port `30902`  

# Dashboard link
http://localhost:8080/api/v1/namespaces/kube-system/services/kubernetes-dashboard:/proxy  

# Error: Path is mounted on but it is not a shared or slave mount.
You have to execute this command on the nodes
```
mount --make-shared PATH
```

# Some useful commands
These are useful for `kubectl get`
`-o wide` shows IP address and node name for pods
`-n namespace` for example `-n kube-system` for system
pods or `-n monitoring` for prometheus.

`kubectl describe resource/RESOURCE_NAME` is essential for debugging.

For getting inside of a container
```
docker exec -it CONTAINER_ID /bin/bash
```
or
```
kubectl exec -it POD_NAME /bin/bash
```
Note: The -it parameters are important  
For learning ip address of docker container
```
docker inspect CONTAINER_ID | grep '"IPAddress"' | head -n 1
```
You can put these into your `.bashrc` like
```
dip() {
  docker inspect $1 | grep '"IPAddress"' | head -n 1
}

dbash() {
  docker exec -it $1 /bin/bash
}
```

# Go install
```
sudo apt install golang-1.9
```
Then add these to .profile
```
export GOPATH="$HOME/workspace/go"
PATH="$PATH:/usr/lib/go-1.9/bin/:$GOPATH:$GOPATH/bin"

```

# Benchmark tool
```
go get -u github.com/rakyll/hey  
hey -z 5m url  
```

# Throwaway docker hub account
Login memorythrowaway  
Password parola  

# Above installs a prometheus with dashboard but for custom metrics re-read below pages
https://github.com/stefanprodan/k8s-prom-hpa  
https://github.com/luxas/kubeadm-workshop  
https://github.com/DirectXMan12/k8s-prometheus-adapter  
https://docs.bitnami.com/kubernetes/how-to/configure-autoscaling-custom-metrics/  
