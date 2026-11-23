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
kubectl create deployment todo-app-dep --image=patrick11211/todo-app:1.2
kubectl set env deployment/todo-app-dep PORT=8080   # optional: change the port
kubectl logs deployment/todo-app-dep
```
