PROJECT=pod-fr-retail
JOB=test
gcloud builds submit --tag gcr.io/$PROJECT/$JOB .