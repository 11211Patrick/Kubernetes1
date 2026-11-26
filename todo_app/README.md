# Todo app

A simple web server that serves an HTML page at `/` with a random image from [Lorem Picsum](https://picsum.photos).

The image is cached in a persistent volume and kept for 10 minutes.
After it expires, the old image is served once more while a new one is downloaded in the background, and the next request gets the new image.
Because the image is stored on a persistent volume, it survives container crashes and pod restarts without calling the API again.

## Endpoints

- `/`: HTML page showing the image
- `/image`: the cached image
- `/shutdown`: stops the process, **for testing only**. The container is restarted automatically by Kubernetes.

## Environment variables

- `PORT`: HTTP port (default: 3000)
- `IMAGE_DIR`: directory where the image is stored (default: `/usr/src/app/files`)
- `CACHE_SECONDS`: how long an image is kept, in seconds (default: 600)
- `IMAGE_URL`: image source (default: `https://picsum.photos/1200`)

## Run locally

```bash
PORT=8080 IMAGE_DIR=/tmp/todo-images python main.py
```

Then open http://localhost:8080 in a browser.

## Build and push the image

```bash
docker build -t patrick11211/todo-app:1.12 .
docker push patrick11211/todo-app:1.12
```

## Create the cluster

The cluster must map host port 8081 to the load balancer's port 80 (used by the Ingress):

```bash
k3d cluster create --port 8082:30080@agent:0 -p 8081:80@loadbalancer --agents 2
```

## Deploy to Kubernetes

The persistent volume and claim (`app-claim`) must be created first (see `../persistent_volume/README.md`).

```bash
kubectl apply -f ../persistent_volume/
kubectl apply -f manifests/
kubectl logs deployment/todo-app-dep
```

## Access

Open http://localhost:8081 in a browser.

## Test persistence

Crash the container (the pod stays, the container restarts):

```bash
curl localhost:8081/shutdown
kubectl get pods -l app=todo-app
```

Replace the whole pod:

```bash
kubectl delete pod -l app=todo-app
```

In both cases the same image is shown after the application is back.