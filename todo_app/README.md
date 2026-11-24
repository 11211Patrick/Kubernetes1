# Todo app

A simple web server that serves an HTML page at `/`.
Prints `Server started in port NNNN` on startup.
The port is set by the environment variable `PORT` (default: 3000).

## Run locally

```bash
PORT=8080 python main.py
```

Then open http://localhost:8080 in a browser.

## Build and push the image

```bash
docker build -t patrick11211/todo-app:1.5 .
docker push patrick11211/todo-app:1.5
```

## Create the cluster

The cluster must map host port 8081 to the load balancer's port 80 (used by the Ingress):

```bash
k3d cluster create --port 8082:30080@agent:0 -p 8081:80@loadbalancer --agents 2
```

## Deploy to Kubernetes

```bash
kubectl apply -f manifests/
kubectl logs deployment/todo-app-dep
```

## Access

Open http://localhost:8081 in a browser.