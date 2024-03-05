# billboard-200-pipeline

Link to data
https://www.dropbox.com/s/ahog97hcatpiddk/billboard-200.db?dl=1

Todo List
- Create GCP Project x
- Install Terraform x

https://docs.mage.ai/production/deploying-to-cloud/using-terraform
- setup terraform using link above (git clone + docker pull)

https://docs.mage.ai/production/deploying-to-cloud/gcp/setup
- setup gcp + docker with mage

- Setup Mage & Docker
    - Download data from link
    - Run Pyspark for batch processing*
    - Partition and convert to parquet
    - Move to DL (GCS)
    - DBT to transform (set schemas, join tables)
        - Install DBT via Docker: https://docs.getdbt.com/docs/core/docker-install
    - Move to DWH (BQ)

- Scheduling
    - Create option to process all or chunk / day
    - Default for chunk / day
    - Assign partitions id
    - Start count when project deployed
    - Each day, advance count