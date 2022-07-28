cd dataops
git add .
git commit -m "update"
git push -u origin master

# Connect to your gke cluster and apply a job
gcloud container clusters get-credentials autopilot-cluster-2 --region europe-west1 --project pod-fr-retail
kubectl apply -f job.yaml 

# Build and deploy your Cloud Run Service to trigger a job on GKE (test it with curl or pubsub)
cd run-k8s-jobs
PROJECT=pod-fr-retail
JOB=run-k8s-jobs
gcloud config set project $PROJECT
gcloud builds submit --tag europe-west1-docker.pkg.dev/$PROJECT/demok8/$JOB
gcloud run deploy $JOB \
--image=europe-west1-docker.pkg.dev/$PROJECT/demok8/$JOB:latest \
--platform=managed \
--region=europe-west1 \
--project=pod-fr-retail

# Trigger your Cloud Run Service or copy run_params.json in your pubsub trigger (see: pubsub-cloud-run-jobs)
curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" -H "Content-Type: application/json"  -d @run_params.json https://run-k8s-jobs-454dfk63ya-ew.a.run.app
gcloud pubsub topics publish projects/pod-fr-retail/topics/pubsub-cloud-run-jobs \
  --message={copy run_params.json}