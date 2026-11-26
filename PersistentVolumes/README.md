# Persistent volumes

PersistentVolumes and PersistentVolumeClaims used by the applications.
They are kept separate from the applications because persistent volumes are usually managed by cluster administrators and are not specific to one application.

| Claim | Node directory | Used by |
|---|---|---|
| `string-claim` | `/tmp/kube` | Ping-pong (writes the request count) and Log output (reads it) |
| `app-claim` | `/tmp/kube2` | Todo app (caches the image) |

All volumes are `local` volumes on the node `k3d-k3s-default-agent-0` with access mode `ReadWriteOnce`.
Because of `nodeAffinity`, every pod using these claims is scheduled to that node.

## Setup

Create the directories on the node first:

```bash
docker exec k3d-k3s-default-agent-0 mkdir -p /tmp/kube /tmp/kube2
```

Then create the volumes and claims:

```bash
kubectl apply -f .
```

## Verify

```bash
kubectl get pv,pvc
```

All volumes and claims should have the status `Bound`.

## Inspect the stored data

```bash
docker exec k3d-k3s-default-agent-0 cat /tmp/kube/pingpong.txt
docker exec k3d-k3s-default-agent-0 ls -l /tmp/kube2
```

## Note

The data is stored inside the k3d node container, so it is lost if the cluster is deleted (`k3d cluster delete`).