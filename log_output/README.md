# Log output

The application runs as two containers in a single pod, sharing an `emptyDir` volume:

- **generate-string**: generates a random string on startup and appends a line with a timestamp and the random string to a file every 5 seconds.
- **read-string**: serves `/status`, which shows the latest line from that file and the number of ping-pongs.

The number of ping-pongs is fetched over HTTP from the Ping-pong application's `/pings` endpoint, through the Service `ping-pong-svc`.

Example response:

```
2026-11-27T08:40:00.123Z: 0ebf4bba-1b04-42e2-b5e6-d3fe7beb8254.
Ping / Pongs: 3
```

If the Ping-pong application is not reachable, the count is shown as `unavailable`.

## Environment variables

- `FILE_PATH`: path of the shared file (default: `/usr/src/app/files/log.txt`), used by both containers
- `PORT`: HTTP port of read-string (default: 3000)
- `PINGPONG_URL`: URL of the ping count (default: `http://ping-pong-svc:2346/pings`)

## Run locally

Start the Ping-pong application first (see `../ping_pong/README.md`), then run each command in a separate terminal.
Use port 3001 for read-string, because Ping-pong already uses 3000:

```bash
FILE_PATH=/tmp/log.txt python generate_string/main.py
```

```bash
FILE_PATH=/tmp/log.txt PORT=3001 PINGPONG_URL=http://localhost:3000/pings python read_string/main.py
```

```bash
curl localhost:3001/status
```

## Build and push the images

```bash
docker build -t patrick11211/generate-string:1.10 generate_string
docker build -t patrick11211/read-string:2.1 read_string
docker push patrick11211/generate-string:1.10
docker push patrick11211/read-string:2.1
```

## Create the cluster

The cluster must map host port 8081 to the load balancer's port 80 (used by the Ingress):

```bash
k3d cluster create --port 8082:30080@agent:0 -p 8081:80@loadbalancer --agents 2
```

## Deploy to Kubernetes

The Ping-pong application must also be deployed (see `../ping_pong/README.md`).

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