# Todo app

A web server that renders the todo app page at `/` (server-side rendering). The page contains:

- a random image from [Lorem Picsum](https://picsum.photos), cached in a persistent volume
- a form for creating a new todo (max 140 characters), which is submitted to the todo-backend
- the list of todos, fetched from the todo-backend inside the cluster

## How it works

1. The browser submits the form with `POST /todos`. The Ingress routes it to the todo-backend, which saves the todo and redirects the browser back to `/`.
2. When rendering `/`, the todo-app fetches the todos from `http://todo-backend-svc:2345/todos` inside the cluster and renders them into the HTML.

The image is kept for 10 minutes. After it expires, the old image is served once more while a new one is downloaded in the background, and the next request gets the new image.
Because the image is stored on a persistent volume, it survives container crashes and pod restarts without calling the API again.

## Endpoints

- `/`: the todo app page
- `/image`: the cached image
- `/shutdown`: stops the process, **for testing only**. The container is restarted automatically by Kubernetes.

## Environment variables

- `PORT`: HTTP port (default: 3000)
- `TODO_BACKEND_URL`: URL of the todo list (default: `http://todo-backend-svc:2345/todos`)
- `IMAGE_DIR`: directory where the image is stored (default: `/usr/src/app/files`)
- `CACHE_SECONDS`: how long an image is kept, in seconds (default: 600)
- `IMAGE_URL`: image source (default: `https://picsum.photos/1200`)

## Run locally

Start the todo-backend first (see `../todo_backend/README.md`), then:

```bash
PORT=8080 IMAGE_DIR=/tmp/todo-images TODO_BACKEND_URL=http://localhost:3000/todos python main.py
```

Open http://localhost:8080 in a browser.
Note that the form posts to `/todos` on the same address, so submitting it only works when running in the cluster behind the Ingress.

## Build and push the image

```bash
docker build -t patrick11211/todo-app:2.2 .
docker push patrick11211/todo-app:2.2
```

## Create the cluster

The cluster must map host port 8081 to the load balancer's port 80 (used by the Ingress):

```bash
k3d cluster create --port 8082:30080@agent:0 -p 8081:80@loadbalancer --agents 2
```

## Deploy to Kubernetes

The persistent volume and claim (`app-claim`) must be created first (see `../persistent_volume/README.md`), and the todo-backend must be deployed.

```bash
kubectl apply -f ../persistent_volume/
kubectl apply -f ../todo_backend/manifests/
kubectl apply -f manifests/
```

If the pod stays `Pending` and `kubectl get pv` shows `app-pv` as `Released`, delete and recreate the volume:

```bash
kubectl delete pv app-pv
kubectl apply -f ../persistent_volume/
```

## Access

Open http://localhost:8081 in a browser, write a todo and press Send.

## Test persistence of the image

```bash
curl localhost:8081/shutdown
kubectl delete pod -l app=todo-app
```

In both cases the same image is shown after the application is back.