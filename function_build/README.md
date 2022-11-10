# README

Deploy function: run `./deploy.sh`

Delete function:
``` sh
gcloud functions delete python-http-function --gen2 --region us-central1
```

Connect to database:
```sh
gcloud sql connect champaign-apartment-postgresql -d postgres -u postgres
```
