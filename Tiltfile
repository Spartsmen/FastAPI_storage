docker_build('artempyzhov/fastapi_storage', '/root/projects/FastAPI_storage',
live_update=[
    sync('.', '/app'),
    run('poetry install', trigger='./pyproject.toml')])

k8s_yaml('.kube/kubernetes-services.yaml')
k8s_yaml('.kube/deployment.yaml')
k8s_yaml('.kube/postgres-deployment.yaml')
k8s_yaml('.kube/postgres-servises.yaml')



