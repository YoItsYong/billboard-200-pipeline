# billboard-200-pipeline

Link to data
https://www.dropbox.com/s/ahog97hcatpiddk/billboard-200.db?dl=1

Todo List
- Create GCP Project & connect gsutil
- Setup Terraform
git clone https://github.com/mage-ai/mage-ai-terraform-templates.git
    - Review what to replace in variables.tf + main.tf

- Setup Mage & Docker
    - Download data from link
    - Run Pyspark for batch processing*
    - Partition and convert to parquet
    - Move to DL (GCS)
    - DBT to transform (set schemas, join tables)
    - Move to DWH (BQ)

- Scheduling
    - Create option to process all or chunk / day
    - Default for chunk / day
    - Assign partitions id
    - Start count when project deployed
    - Each day, advance count