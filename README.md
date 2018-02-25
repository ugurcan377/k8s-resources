# Kubernetes install
```
git clone git@github.com:Mirantis/kubeadm-dind-cluster.git  
cd kubeadm-dind-cluster  
./fixed/dind-cluster-v1.9.sh up  
```
config.sh for node count and networking  
image/kubelet.service has eviction policies. #Haven't tried it yet  

# Metrics-server install
```
git clone git@github.com:kubernetes-incubator/metrics-server.git  
cd metrics-server  
kubectl create -f deploy/1.8+/  
```
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
# Check
```
kubectl api-versions  
```
Check if following api endpoints exist  
```
metrics.k8s.io/v1beta1  
autoscaling/v2beta1  
```
```
kubectl get --raw "/apis/metrics.k8s.io/v1beta1/nodes"  
```
# Monitoring
```
git clone git@github.com:coreos/prometheus-operator.git  
cd contrib/kube-prometheus/  
hack/cluster-monitoring/deploy  
```
# Dashboard link
http://localhost:8080/api/v1/namespaces/kube-system/services/kubernetes-dashboard:/proxy  

# Benchmark tool
```
go get -u github.com/rakyll/hey  
hey -z 5m url  
```
# Throwaway docker hub account
Login memorythrowaway  
Password parola  

# Above installs a prometheus with dashboard but for custom metrics
# re-read below pages
https://github.com/stefanprodan/k8s-prom-hpa  
https://github.com/luxas/kubeadm-workshop  
https://github.com/DirectXMan12/k8s-prometheus-adapter  
https://docs.bitnami.com/kubernetes/how-to/configure-autoscaling-custom-metrics/  
