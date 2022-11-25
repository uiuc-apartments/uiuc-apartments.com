#!/usr/bin/env bash

if [[ -z "${API_KEY}" ]]; then
  echo "API_KEY not set"
  exit 1
fi


gcloud functions deploy build-apartments \
    --gen2 \
    --runtime=python310 \
    --region=us-central1 \
    --source=. \
    --entry-point=build_apartments \
    --trigger-http \
    --allow-unauthenticated \
    --timeout=1800 \
    --set-env-vars "API_KEY=$API_KEY" \
    --project=champaign-apartment-aggregator
