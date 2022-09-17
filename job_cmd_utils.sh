#gh auth login

cd dataops
git add .
git commit -m "update"
git push -u origin master

# Connect to your gke cluster and apply a job
gcloud container clusters get-credentials autopilot-cluster-2 --region europe-west1 --project pod-fr-retail
kubectl apply -f job-unzip.yaml 

# Deploy Run Jobs - Method 1: Build and deploy your Cloud Run Service to trigger a job on GKE (test it with curl or pubsub)
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

# Deploy Run Jobs - Method 2: Build and deploy your Cloud Run Service to trigger a job on GKE ()
gcloud builds submit --region=europe-west1

# Trigger your Cloud Run Service or copy run_params.json in your pubsub trigger (see: pubsub-cloud-run-jobs)
curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" -H "Content-Type: application/json"  -d @run_params.json https://run-k8s-jobs-454dfk63ya-ew.a.run.app

gcloud pubsub topics publish projects/pod-fr-retail/topics/pubsub-cloud-run-jobs \
  --message=


# Build k8 Jobs - unzip
cd demo_k8_jobs_unzip_gcs
PROJECT=pod-fr-retail
JOB=demo_k8_jobs_unzip_gcs
gcloud config set project $PROJECT
gcloud builds submit --tag europe-west1-docker.pkg.dev/$PROJECT/demok8/$JOB