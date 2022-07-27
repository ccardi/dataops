
cd Jobs/run-k8s-jobs
PROJECT=pod-fr-retail
gcloud config set project $PROJECT

JOB=run-k8s-jobs
PROJECT=pod-fr-retail
gcloud builds submit --tag europe-west1-docker.pkg.dev/$PROJECT/demok8/$JOB

gcloud run deploy $JOB \
--image=europe-west1-docker.pkg.dev/$PROJECT/demok8/$JOB:latest \
--platform=managed \
--region=europe-west1 \
--project=pod-fr-retail

cd ..

curl -H "Authorization: Bearer $(gcloud auth print-identity-token)" -H "Content-Type: application/json"  -d '{"projectId":"pod-fr-retail","region":"europe-west1", "gkeClusterName":"autopilot-cluster-2", "jobStorageBucket":"pod-fr-retail-jobs-conf","jobPathName":"job.yaml", "jobRootName":"pandas-to-bq-"}' https://run-k8s-jobs-454dfk63ya-ew.a.run.app
{"projectId":"pod-fr-retail","region":"europe-west1", "gkeClusterName":"autopilot-cluster-2", "jobStorageBucket":"pod-fr-retail-jobs-conf","jobPathName":"job.yaml", "jobRootName":"pandas-to-bq-"}