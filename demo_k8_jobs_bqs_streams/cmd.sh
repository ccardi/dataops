python3 main.py \
--max_streams=3 \
--bq_projectId='pod-fr-retail' \
--bq_dataset='kaggle' \
--bq_tableId='products_vision_search' \
--spanner_instance='pod-fr-retail-kaggle' \
--spanner_table='products_vision_search/kaggle_shoes/part-' \
--selected_fields='image_uri,image_id,product_set_id,product_id,product_category,product_display_name,labels,poly'


python3 main.py \
--max_streams=10000 \
--bq_projectId='pod-fr-retail' \
--bq_dataset='supply_demo' \
--bq_tableId='virtualshop_orders_sku' \
--spanner_instance='pod-fr-retail-kaggle' \
--spanner_table='products_vision_search/kaggle_shoes/part-' \
--selected_fields='image_uri,image_id,product_set_id,product_id,product_category,product_display_name,labels,poly'

# Build k8 Jobs - unzip
cd demo_k8_jobs_bqs_gcs
PROJECT=pod-fr-retail
JOB=demo_k8_jobs_bqs_gcs
gcloud config set project $PROJECT
gcloud builds submit --tag europe-west1-docker.pkg.dev/$PROJECT/demok8/$JOB