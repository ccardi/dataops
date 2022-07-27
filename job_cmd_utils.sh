cd Jobs/demo_k8_jobs_basic
git add .
git commit -m "update"
git push -u origin master

gcloud container clusters get-credentials autopilot-cluster-2 --region europe-west1 --project pod-fr-retail
kubectl apply -f job.yaml 
