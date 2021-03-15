# vault-demo-app

This demo app is to show static and dynamic database credentials created by vault. It requires that you have deployed postgres database. You can provide the following environment variables to the app.

`PY_DB_CRED_LOCATION` - location of `creds.json` file, end with `/` like `/home/ubuntu/mysecret/`, default same location as `webapp.py`

`PY_APP_DB_NAME` - name of the database, default is `postgres`

`PY_APP_DB_HOST`- hostname of the database, default is `127.0.0.1`

`PY_APP_DB_PORT` - port database is listening to, default is `5432`


Inject the dynamic secret into the app's pod with annotation like this
```
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
```
If you want to test the app locally, create a creds.json file locally to connect to your local postgres database
```
{
  "user":"your-db-username", 
  "pass":"your-db-password"
}
```
