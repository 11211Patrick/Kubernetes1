# Ping-pong

Responds with `pong N` to GET requests on `/pingpong`, where N is a request counter starting from 0.
The counter is kept in memory and resets when the process restarts.
The port is set by the environment variable `PORT` (default: 3000).

## Run locally

```bash
python main.py
curl localhost:3000/pingpong
```

## Build and push the image

```bash
docker build -t patrick11211/ping-pong:1.9 .
docker push patrick11211/ping-pong:1.9
```

## Deploy to Kubernetes

The Ingress is shared with the Log output application (`log_output/manifests/ingress.yaml`).

```bash
kubectl apply -f manifests/
kubectl apply -f ../log_output/manifests/
```

## Access

Open http://localhost:8081/pingpong in a browser.