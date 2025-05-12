# 1. Gestión de Pods
| Comando | Descripción |
|-------|-------|
| kubectl get pods -n <namespace> | Listar todos los pods en un namespace. |
| kubectl describe pod <pod-name> -n <namespace> | Ver detalles de un pod (contenedores, eventos, etc.). |
| kubectl delete pod <pod-name> -n <namespace> | Eliminar un pod específico.
| kubectl delete pod <pod-name> -n <namespace> --force --grace-period=0	| Forzar eliminación de un pod atascado.|
| kubectl logs <pod-name> -c <container-name> -n <namespace> | Ver logs de un contenedor dentro de un pod.|
| kubectl exec -it <pod-name> -n <namespace> -- /bin/sh	| Acceder a la shell de un contenedor en un pod.|
# 2. Despliegue de Pods Temporales
| Comando | Descripción |
|-------|-------|
| kubectl run <pod-name> --rm -it --image=<image> --namespace=<ns> -- /bin/sh | Crear un pod temporal interactivo (ej: busybox).|
| kubectl run debug --rm -it --image=nicolaka/netshoot -- /bin/bash | Pod temporal con herramientas de red (netshoot).|
# 3. Gestión de Deployments/StatefulSets
| Comando | Descripción |
|-------|-------|
| kubectl get deployments -n <namespace> | Listar deployments. |
| kubectl delete deployment <deploy-name> -n <namespace> | Eliminar un deployment y sus pods. |
| kubectl scale deployment <deploy-name> --replicas=0 -n <namespace> | Detener un deployment (escalar a 0 pods). |
| kubectl get statefulsets -n <namespace> | Listar statefulsets. |
# 4. ConfigMaps y Servicios
| Comando | Descripción |
|-------|-------|
| kubectl create configmap <name> --from-file=<path> -n <namespace> | Crear un ConfigMap desde un archivo. |
| kubectl get configmaps -n <namespace> | Listar ConfigMaps. |
| kubectl expose deployment <name> --type=NodePort --port=<port> | Exponer un servicio como NodePort. |
# 5. Namespaces
| Comando | Descripción |
|-------|-------|
| kubectl get namespaces o kubectl get ns | Listar todos los namespaces. |
| kubectl create namespace <name> | Crear un namespace. |
| kubectl delete namespace <name> | Eliminar un namespace (¡cuidado!). |
# 6. Comandos Adicionales Útiles
| Comando | Descripción |
|-------|-------|
| kubectl get all -n <namespace> | Listar todos los recursos en un namespace.|
| kubectl cluster-info | Ver información del cluster.|
| kubectl apply -f <file.yaml> | Aplicar un manifiesto YAML.|
| kubectl delete -f <file.yaml> | Eliminar recursos definidos en un YAML.|
# 7. Si se queda atascado en 'Terminating' un namespace que se eliminó
| Comando | Descripción |
|-------|-------|
| kubectl get namespace NombreNamespace -o json > NombreNamespace.json | Guardar la configuración del namespace|
| vi NombreNamespace.json | Modificar la sección "spec" para que "finalizers" quede vacio: [] |
| kubectl replace --raw "/api/v1/namespaces/NombreNamespace/finalize" -f NombreNamespace.json | aplicar el archivo, esto debe terminar de eliminar el namespace |
# 8. Agregar una imagen Docker local a k3s
| Comando | Descripción |
|-------|-------|
| docker build -t python-server-listener:1.0 . | Ya teniendo el Dockerfile, crear la imagen local|
| docker save -o python-server-listener.tar python-server-listener:1.0 | Salvar la imagen como un .tar|
| sudo k3s ctr images import python-server-listener.tar | Exportar la imagen a k3s|