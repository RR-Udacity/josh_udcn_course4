vagrant up
vagrant plugin install vagrant-scp

# Bring k3s context to local machine
vagrant scp default:/etc/rancher/k3s/k3s.yaml ~/.kube/config

# Prometheus
kubectl create namespace monitoring
helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
helm repo add stable https://charts.helm.sh/stable
helm repo update
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --version 31.0.2

# Jaeger
kubectl create namespace observability
kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.28.0/deploy/crds/jaegertracing.io_jaegers_crd.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.28.0/deploy/service_account.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.28.0/deploy/role.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.28.0/deploy/role_binding.yaml
kubectl create -n observability -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.28.0/deploy/operator.yaml
kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.28.0/deploy/cluster_role.yaml
kubectl create -f https://raw.githubusercontent.com/jaegertracing/jaeger-operator/v1.28.0/deploy/cluster_role_binding.yaml
kubectl apply -f ./manifests/app/

sleep 30
# Port-Forward Grafana
kubectl port-forward -n monitoring (kubectl get po -n monitoring | grep grafana | awk '{print $1}') 3000 &

# Port-Forward Prometheus
kubectl port-forward -n monitoring (kubectl get po -n monitoring | grep prometheus-kube-prometheus-prometheus | awk '{print $1}') 9090 &

# Port-Forward Frontend
kubectl port-forward svc/frontend 8082:8082 &

# Port-Forward Backend
kubectl port-forward svc/backend 8081:8081 &

# Port-Forward Trial
kubectl port-forward svc/trial 8083:8083 &

# see the background tasks running with the `jobs` command