# Log output
The application runs as two containers in a single pod, sharing an `emptyDir` volume:
- **generate-string**: generates a random string on startup and writes a line with the random string and timestamp every 5 seconds into a file.
- **read-string**: reads that file and provides the content in the HTTP GET endpoint for the user to see
The port is set by the environment variable `PORT` (default: 3000).

Environment variables:

- `FILE_PATH`: path of the shared file (default: `/usr/src/app/files/log.txt`), used by both containers.
- `PORT`: HTTP port of read-string (default: 3000).

Note: the file is stored in an `emptyDir` volume, so its content is lost when the pod is replaced.

## Run locally

Run each command in a separate terminal:

```bash
FILE_PATH=/tmp/log.txt python generate_string/main.py
```

```bash
FILE_PATH=/tmp/log.txt python read_string/main.py
```

```bash
curl localhost:3000/status
```

## Build and push the image

```bash
docker build -t patrick11211/generate-string:1.10 generate_string
docker build -t patrick11211/read-string:1.10 read_string
docker push patrick11211/generate-string:1.10
docker push patrick11211/read-string:1.10
```

## Deploy to Kubernetes

The cluster must map host port 8081 to the load balancer's port 80 (used by the Ingress):

```bash
k3d cluster create --port 8082:30080@agent:0 -p 8081:80@loadbalancer --agents 2
```

```bash
kubectl apply -f manifests/
```

View the logs of each container:

```bash
kubectl logs deployment/log-output-dep -c generate-string
kubectl logs deployment/log-output-dep -c read-string
```

## Access

Open http://localhost:8081/status in a browser.