#!/bin/bash
python3 main.py \
--runner=DataflowRunner \
--project pod-fr-retail \
--input gs://pod-fr-retail-kering/report_ids/ids.csv \
--output gs://pod-fr-retail-kering/test \
--staging_location gs://pod-fr-retail-kering/staging \
--temp_location gs://pod-fr-retail-kering/temp \
--zone europe-west1-c \
--region europe-west1 \
--worker_machine_type n1-standard-1 \
--num_workers 2 \
--max_num_workers 3 \
--url 'https://opendata.paris.fr/api/records/1.0/search/?dataset=reseau-cyclable&facet=typologie_simple&facet=bidirectionnel&facet=statut&facet=sens_velo&facet=voie&facet=arrdt&facet=bois&facet=position&facet=circulation&facet=piste&facet=couloir_bus&facet=type_continuite&facet=reseau&facet=date_de_livraison&refine.typologie=PISTE+CYCLABLE+SUR+CHAUSSEE&refine.typologie=PISTE+CYCLABLE+SUR+TROTTOIR'