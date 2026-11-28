# Persistent volumes

PersistentVolumes and PersistentVolumeClaims used by the applications.
They are kept separate from the applications because persistent volumes are usually managed by cluster administrators and are not specific to one application.

| Claim | Namespace | Node directory | Used by |
|---|---|---|---|
| `string-claim` | `default` | `/tmp/kube` | Not used since exercise 2.1 |
| `app-claim` | `project` | `/tmp/kube2` | Todo app (caches the image) |

PersistentVolumes are cluster-scoped, while each claim belongs to a namespace and can only be used by pods in the same namespace.

All volumes are `local` volumes on the node `k3d-k3s-default-agent-0` with access mode `ReadWriteOnce`.
Because of `nodeAffinity`, every pod using these claims is scheduled to that node.

## Setup

Create the directories on the node and the namespaces first:

```bash
docker exec k3d-k3s-default-agent-0 mkdir -p /tmp/kube /tmp/kube2
kubectl apply -f ../namespaces/
```

Then create the volumes and claims:

```bash
kubectl apply -f .
```

## Verify

```bash
kubectl get pv
kubectl get pvc -A
```

All volumes and claims should have the status `Bound`.

## A claim stays Pending

A `local` volume is not bound again automatically after its claim is deleted; it stays `Released`.
Delete and recreate the volume. The files in the node directory are kept.

```bash
kubectl delete pv app-pv
kubectl apply -f .
```

## Inspect the stored data

```bash
docker exec k3d-k3s-default-agent-0 ls -l /tmp/kube2
```

## Note

The data is stored inside the k3d node container, so it is lost if the cluster is deleted (`k3d cluster delete`).