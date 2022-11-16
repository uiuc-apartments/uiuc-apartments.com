#!/usr/bin/env sh

gcloud functions deploy build-apartments \
    --gen2 \
    --runtime=python310 \
    --region=us-central1 \
    --source=. \
    --entry-point=build_apartments \
    --trigger-http \
    --allow-unauthenticated \
    --timeout=900 \
    --set-env-vars "API_KEY=$API_KEY" \
    --project=champaign-apartment-aggregator
