# Todo app

A simple web server. Prints `Server started in port NNNN` on startup.
The port is set by the environment variable `PORT` (default: 3000).

## Run locally

```bash
PORT=8080 python main.py
```

## Build and push the image

```bash
docker build -t patrick11211/todo-app:1.2 .
docker push patrick11211/todo-app:1.2
```

## Deploy to Kubernetes

```bash
kubectl apply -f manifests/deployment.yaml
kubectl logs -f deployment/log-output-dep
```

## Access

```bash
kubectl port-forward deployment/todo-app-dep 8080:8080
```

Then open http://localhost:8080 in a browser.