# Fixes to Project 3 Install

## Vagrantfile

add port forward `6443` to Vagrantfile

## Local Context

Jump back to local machine and copy the contents of vm>`/etc/rancher/k3s/k3s.yaml` to local>`~/.kube/config` in order to use kubectl locally, run and install services that way.

## Prometheus

```bash
helm install prometheus prometheus-community/kube-prometheus-stack --namespace monitoring --version 31.0.2
```

## Jaeger

```yaml
kind: ClusterRoleBinding
apiVersion: rbac.authorization.k8s.io/v1
metadata:
  name: jaeger-operator-with-auth-delegator
  namespace: observability
subjects:
- kind: ServiceAccount
  name: jaeger-operator
  namespace: observability
roleRef:
  kind: ClusterRole
  name: system:auth-delegator
  apiGroup: rbac.authorization.k8s.io
```

```bash
kubectl create namespace observability
kubectl create -f https://github.com/jaegertracing/jaeger-operator/releases/download/v1.30.0/jaeger-operator.yaml -n observability
kubectl create -f {above code}
```
