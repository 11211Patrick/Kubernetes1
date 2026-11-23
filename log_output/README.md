# Log output

Generates a random string (UUID) on startup, keeps it in memory, and prints it with a timestamp every 5 seconds.

## Run locally

```bash
python main.py
```

## Build and push the image

```bash
docker build -t patrick11211/log-output:1.1 .
docker push patrick11211/log-output:1.1
```

## Deploy to Kubernetes

```bash
kubectl create deployment log-output-dep --image=patrick11211/log-output:1.1
kubectl logs -f deployment/log-output-dep
```
