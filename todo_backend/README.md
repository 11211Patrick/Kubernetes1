# Todo backend

A service that stores todo items in memory.
The todos are lost when the process restarts; a database will be added later.

The service runs in the namespace `project`.

## Endpoints

- `GET /todos`: returns the list of todos as JSON, for example `["Learn Kubernetes"]`.
- `POST /todos`: creates a new todo from a form field `todo`, then redirects the browser to `REDIRECT_URL` with status 303.
  Requests with an empty todo or a todo longer than `TODO_MAX_LENGTH` are rejected with status 400.

## Configuration

All configuration is passed as environment variables. There are no default values in the source code;
the service exits with an error message if a variable is missing.

| Variable | Description | Value in the cluster |
|---|---|---|
| `PORT` | HTTP port | `3000` |
| `TODO_MAX_LENGTH` | Maximum length of a todo | `140` |
| `REDIRECT_URL` | Where the browser is redirected after creating a todo | `/` |

In the cluster, the values are defined in the ConfigMap `todo-backend-config` (`manifests/configmap.yaml`)
and passed to the container with `envFrom`.
`PORT` must match the `targetPort` of the Service.

## Run locally

```bash
PORT=3000 TODO_MAX_LENGTH=140 REDIRECT_URL=/ python main.py
```

In another terminal:

```bash
curl -i -X POST -d "todo=Learn Kubernetes" localhost:3000/todos
curl localhost:3000/todos
```

## Build and push the image

```bash
docker build -t patrick11211/todo-backend:2.6 .
docker push patrick11211/todo-backend:2.6
```

## Deploy to Kubernetes

The namespace must be created first (see `../namespaces/README.md`).
The Service `todo-backend-svc` exposes the service inside the namespace on port 2345.
The path `/todos` is routed to this service by the Ingress defined in `../todo_app/manifests/ingress.yaml`.

```bash
kubectl apply -f ../namespaces/
kubectl apply -f manifests/
```

Check the status, logs and configuration:

```bash
kubectl get pods -n project
kubectl logs deployment/todo-backend-dep -n project
kubectl exec deployment/todo-backend-dep -n project -- printenv PORT TODO_MAX_LENGTH REDIRECT_URL
```

After changing the ConfigMap, restart the pod to apply the new values:

```bash
kubectl rollout restart deployment/todo-backend-dep -n project
```

## Access

```bash
curl localhost:8081/todos
```