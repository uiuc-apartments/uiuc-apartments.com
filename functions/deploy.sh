#!/usr/bin/env sh

gcloud functions deploy python-http-function \
--gen2 \
    --runtime=python310 \
    --region=us-central1 \
    --source=. \
    --entry-point=hello_get \
    --trigger-http \
    --allow-unauthenticated
