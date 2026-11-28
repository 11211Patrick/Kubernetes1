# Ping-pong

A simple HTTP server with a request counter kept in memory.
The counter resets when the process restarts.

The application runs in the namespace `exercises`.

## Endpoints

- `/pingpong`: responds with `pong N` and increases the counter. Exposed to browsers through the Ingress.
- `/pings`: responds with the current counter value without increasing it. Used by the Log output application inside the cluster; not exposed through the Ingress.

## Environment variables

- `PORT`: HTTP port (default: 3000)

## Run locally

```bash
python main.py
```

In another terminal:

```bash
curl localhost:3000/pingpong
curl localhost:3000/pings
```

## Build and push the image

```bash
docker build -t patrick11211/ping-pong:2.1 .
docker push patrick11211/ping-pong:2.1
```

## Deploy to Kubernetes

The namespace must be created first (see `../namespaces/README.md`).
The Service `ping-pong-svc` exposes the application inside the namespace on port 2346.
The Ingress is shared with the Log output application and defined in `../log_output/manifests/ingress.yaml`.

```bash
kubectl apply -f ../namespaces/
kubectl apply -f manifests/
kubectl apply -f ../log_output/manifests/
```

Check the status and logs:

```bash
kubectl get pods -n exercises
kubectl logs deployment/ping-pong-dep -n exercises
```

## Access

Open http://localhost:8081/pingpong in a browser. The number increases on every request.