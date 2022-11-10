#!/usr/bin/env sh

gcloud functions deploy get-apartments \
--gen2 \
    --runtime=python310 \
    --region=us-central1 \
    --source=. \
    --entry-point=get_apartments \
    --trigger-http \
    --allow-unauthenticated \
    --project=champaign-apartment-aggregator
