# vault-demo-app

This demo app is to show static and dynamic database credentials created by vault in Kubernetes. It requires that you have deployed and configured vault and postgres database.

**Vault and postgres installation with helm**

https://www.vaultproject.io/docs/platform/k8s/helm/run

```
helm repo add hashicorp https://helm.releases.hashicorp.com
helm search repo hashicorp/vault -l
helm install vault hashicorp/vault --version 0.9.1
```

https://github.com/bitnami/charts/tree/master/bitnami/postgresql/

```
helm repo add bitnami https://charts.bitnami.com/bitnami
helm install postgres \
  --set postgresqlPassword=secretpassword,postgresqlDatabase=my-database \
    bitnami/postgresql
```

**Configure vault with dynamic secret for postgres database**

https://learn.hashicorp.com/tutorials/vault/database-secrets


**Configuring the application**

Build the app image with provided Dockerfile and push to your registry such as dockerhub 
```
docker image build -t <your-user>/<app-name>:<version> .
docker push <your-user>/<app-name>:<version>
```

Reference your app in your kubernetes deployment file. 

```
apiVersion: apps/v1
kind: Deployment
metadata:
  name: web-deployment
  labels:
    app: web
spec:
  replicas: 2
  selector:
    matchLabels:
      app: web
  template:
    metadata:
      labels:
        app: web
      annotations:     
        vault.hashicorp.com/agent-inject: "true"
        vault.hashicorp.com/agent-inject-secret-creds.json: "database/creds/python-app"
        vault.hashicorp.com/agent-inject-template-creds.json: |
          {
          {{ with secret "database/creds/python-app" -}}
            "user":"{{ .Data.username }}", 
            "pass":"{{ .Data.password }}"
          {{- end }}
          }
        vault.hashicorp.com/role: "web"
    spec:
      serviceAccountName: web
      containers:
        - name: web
          image: <your-user>/<app-name>:<version>
          ports:
            - containerPort: 5000
          env:
            - name: "PY_DB_CRED_LOCATION"
              value: "/vault/secrets/"
            - name: "PY_APP_DB_HOST"
              value: "postgres" 
```

*WARNING: DO NOT expose this app with load balancer as the app will display your database username and password*

You can provide the following environment variables to the app.

`PY_DB_CRED_LOCATION` - location of `creds.json` file, end with `/` like `/home/ubuntu/mysecret/`, default is same location as `webapp.py`. The app expects `user` and `pass` variables defined in `creds.json` file as json

```
{
  "user":"your-db-username", 
  "pass":"your-db-password"
}
```

`PY_APP_DB_NAME` - name of the database, default is `postgres`

`PY_APP_DB_HOST`- hostname of the database, default is `127.0.0.1`

`PY_APP_DB_PORT` - port database is listening to, default is `5432`

Once the app is deployed, use port-forwarding to map your kubernetes service to local port. 
```
kubectl port-forward service/app-service 5000:5000
```
Browse `localhost:5000` to see that dynamic credentials are being used.

If you want to test the app locally, create a creds.json file locally to connect to your local postgres database
```
{
  "user":"your-db-username", 
  "pass":"your-db-password"
}
```
