python3 main.py \
--max_rows=20000 \
--projectId='pod-fr-retail' \
--dataset='kaggle' \
--tableId='products_vision_search' \
--bucket_name='pod-fr-retail-kaggle' \
--file_prefix='products_vision_search/kaggle_shoes/part-' \
--selected_fields='image_uri,image_id,product_set_id,product_id,product_category,product_display_name,labels,poly'