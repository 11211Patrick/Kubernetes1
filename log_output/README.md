# Log output

Generates a random string (UUID) on startup, keeps it in memory, and prints it with a timestamp every 5 seconds.

## Run locally

```bash
python main.py
curl localhost:3000/status
```

## Build and push the image

```bash
docker build -t patrick11211/log-output:1.7 .
docker push patrick11211/log-output:1.7
```

## Create the cluster

The cluster must map host port 8081 to the load balancer's port 80 (used by the Ingress):
```bash
k3d cluster create --port 8082:30080@agent:0 -p 8081:80@loadbalancer --agents 2
```

## Deploy to Kubernetes

```bash
kubectl apply -f manifests/
kubectl logs -f deployment/log-output-dep
```

## Access

Open http://localhost:8081/status in a browser.