# Todo app

A web server that renders the todo app page at `/` (server-side rendering). The page contains:

- a random image from [Lorem Picsum](https://picsum.photos), cached in a persistent volume
- a form for creating a new todo, which is submitted to the todo-backend
- the list of todos, fetched from the todo-backend inside the cluster

The application runs in the namespace `project`.

## How it works

1. The browser submits the form with `POST /todos`. The Ingress routes it to the todo-backend, which saves the todo and redirects the browser back to `/`.
2. When rendering `/`, the todo-app fetches the todos from the todo-backend inside the namespace and renders them into the HTML.

The image is kept for `CACHE_SECONDS` seconds. After it expires, the old image is served once more while a new one is downloaded in the background, and the next request gets the new image.
Because the image is stored on a persistent volume, it survives container crashes and pod restarts without calling the API again.

## Endpoints

- `/`: the todo app page
- `/image`: the cached image
- `/shutdown`: stops the process, **for testing only**. The container is restarted automatically by Kubernetes.

## Configuration

All configuration is passed as environment variables. There are no default values in the source code;
the application exits with an error message if a variable is missing.

| Variable | Description | Value in the cluster |
|---|---|---|
| `PORT` | HTTP port | `8080` |
| `TODO_BACKEND_URL` | URL for fetching the todos inside the cluster | `http://todo-backend-svc:2345/todos` |
| `TODO_POST_URL` | URL the browser submits the form to (routed by the Ingress) | `/todos` |
| `TODO_MAX_LENGTH` | Maximum length of a todo in the form | `140` |
| `IMAGE_DIR` | Directory where the image is stored | `/usr/src/app/files` |
| `IMAGE_URL` | Image source | `https://picsum.photos/1200` |
| `CACHE_SECONDS` | How long an image is kept, in seconds | `600` |

In the cluster, the values are defined in the ConfigMap `todo-app-config` (`manifests/configmap.yaml`)
and passed to the container with `envFrom`.
`PORT` must match the `targetPort` of the Service, and `TODO_MAX_LENGTH` should be the same as in the todo-backend.

## Run locally

Start the todo-backend first (see `../todo_backend/README.md`), then:

```bash
PORT=8080 \
TODO_BACKEND_URL=http://localhost:3000/todos \
TODO_POST_URL=/todos \
TODO_MAX_LENGTH=140 \
IMAGE_DIR=/tmp/todo-images \
IMAGE_URL=https://picsum.photos/1200 \
CACHE_SECONDS=600 \
python main.py
```

Open http://localhost:8080 in a browser.
To submit the form locally without the Ingress, set `TODO_POST_URL=http://localhost:3000/todos` and `REDIRECT_URL=http://localhost:8080/` for the todo-backend.

## Build and push the image

```bash
docker build -t patrick11211/todo-app:2.6 .
docker push patrick11211/todo-app:2.6
```

## Create the cluster

The cluster must map host port 8081 to the load balancer's port 80 (used by the Ingress):

```bash
k3d cluster create --port 8082:30080@agent:0 -p 8081:80@loadbalancer --agents 2
```

## Deploy to Kubernetes

The namespace, the persistent volume and claim (`app-claim`) must be created first, and the todo-backend must be deployed:

```bash
kubectl apply -f ../namespaces/
kubectl apply -f ../persistent_volume/
kubectl apply -f ../todo_backend/manifests/
kubectl apply -f manifests/
```

Check the status, logs and configuration:

```bash
kubectl get pods -n project
kubectl logs deployment/todo-app-dep -n project
kubectl exec deployment/todo-app-dep -n project -- printenv
```

After changing the ConfigMap, restart the pod to apply the new values:

```bash
kubectl rollout restart deployment/todo-app-dep -n project
```

If the pod stays `Pending` and `kubectl get pv` shows `app-pv` as `Released`, see `../persistent_volume/README.md`.

## Access

Open http://localhost:8081 in a browser, write a todo and press Send.

## Test persistence of the image

```bash
curl localhost:8081/shutdown
kubectl delete pod -l app=todo-app -n project
```

In both cases the same image is shown after the application is back.