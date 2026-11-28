# Todo backend

A service that stores todo items in memory.
The todos are lost when the process restarts; a database will be added later.

The service runs in the namespace `project`.

## Endpoints

- `GET /todos`: returns the list of todos as JSON, for example `["Learn Kubernetes"]`.
- `POST /todos`: creates a new todo from a form field `todo` (1-140 characters), then redirects the browser to `/` with status 303.
  Requests with an empty or too long todo are rejected with status 400.

## Environment variables

- `PORT`: HTTP port (default: 3000)

## Run locally

```bash
python main.py
```

In another terminal:

```bash
curl -i -X POST -d "todo=Learn Kubernetes" localhost:3000/todos
curl localhost:3000/todos
```

## Build and push the image

```bash
docker build -t patrick11211/todo-backend:2.2 .
docker push patrick11211/todo-backend:2.2
```

## Deploy to Kubernetes

The namespace must be created first (see `../namespaces/README.md`).
The Service `todo-backend-svc` exposes the service inside the namespace on port 2345.
The path `/todos` is routed to this service by the Ingress defined in `../todo_app/manifests/ingress.yaml`.

```bash
kubectl apply -f ../namespaces/
kubectl apply -f manifests/
```

Check the status and logs:

```bash
kubectl get pods -n project
kubectl logs deployment/todo-backend-dep -n project
```

## Access

```bash
curl localhost:8081/todos
```