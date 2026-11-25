# Ping-pong

Responds with `pong N` to GET requests on `/pingpong`, where N is the number of requests received so far, starting from 0.

The counter is saved to a file on a persistent volume after every request, and loaded from that file on startup.
This means the count survives pod restarts, and the Log output application can read it from the same volume.

Environment variables:

- `PORT`: HTTP port (default: 3000).
- `COUNT_FILE`: path of the counter file (default: `/usr/src/app/files/pingpong.txt`).

## Run locally

```bash
COUNT_FILE=/tmp/pingpong.txt python main.py
```

In another terminal:

```bash
curl localhost:3000/pingpong
```

## Build and push the image

```bash
docker build -t patrick11211/ping-pong:1.11 .
docker push patrick11211/ping-pong:1.11
```

## Deploy to Kubernetes

The persistent volume and claim must be created first (see `../persistent_volume/README.md`).
The deployment mounts the claim `string-claim` at `/usr/src/app/files`.

```bash
kubectl apply -f ../persistent_volume/
kubectl apply -f manifests/
kubectl apply -f ../log_output/manifests/
```

The Ingress is shared with the Log output application and defined in `../log_output/manifests/ingress.yaml`.

## Access

Open http://localhost:8081/pingpong in a browser. The number increases on every request.

## Verify that the count persists

```bash
kubectl delete pod -l app=ping-pong
curl localhost:8081/pingpong
```

After the new pod starts, the count continues from the previous value instead of resetting to 0.