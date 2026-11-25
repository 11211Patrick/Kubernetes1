# Persistent volume

A PersistentVolume and a PersistentVolumeClaim shared by the Ping-pong and Log output applications.
They are kept separate from the applications because persistent volumes are usually managed by cluster administrators and are not specific to one application.

- **PersistentVolume**: a `local` volume backed by the directory `/tmp/kube` on the node `k3d-k3s-default-agent-0`.
- **PersistentVolumeClaim** (`string-claim`): requests 1Gi with access mode `ReadWriteOnce`, and is bound to the volume above.

Because the volume exists only on `k3d-k3s-default-agent-0` (set by `nodeAffinity`), every pod that uses the claim is scheduled to that node.

## Setup

Create the directory on the node first:

```bash
docker exec k3d-k3s-default-agent-0 mkdir -p /tmp/kube
```

Then create the volume and the claim:

```bash
kubectl apply -f .
```

## Verify

```bash
kubectl get pv,pvc
```

Both should have the status `Bound`.

## Inspect the stored data

```bash
docker exec k3d-k3s-default-agent-0 cat /tmp/kube/pingpong.txt
```

## Note

The data is stored inside the k3d node container, so it is lost if the cluster is deleted (`k3d cluster delete`).