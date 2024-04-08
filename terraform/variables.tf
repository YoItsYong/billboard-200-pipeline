variable "credentials" {
    description = "My Credentials"
    default = "./path/to/gcs_key.json"
}
variable "project" {
    description = "Project"
    default = "billboard-200-project-2"
}

variable "region" {
    description = "Region"
    default = "us-central1"
}

variable "location" {
    description = "Project Location"
    default = "US"
}

variable "bq_dataset_name" {
    description = "My BigQuery Dataset Name"
    default = "bb200_data-2"
}

variable "gcs_bucket_name" {
    description = "My Storage Bucket Name"
    default = "bb200-2"
}

variable "gcs_storage_class" {
  description = "Bucket Storage Class"
  default = "STANDARD"
}

variable "dp_cluster_name" {
    description = "Dataproc Cluster Name"
    default = "music-chart-cluster-2"
}