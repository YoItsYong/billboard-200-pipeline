terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "5.12.0"
    }
  }
}

provider "google" {
  # Configuration options
  credentials   = file(var.credentials)
  project       = var.project
  region        = var.region
}

resource "google_storage_bucket" "bb200_bucket" {
  name          = var.gcs_bucket_name
  location      = var.location
  storage_class = var.gcs_storage_class
  force_destroy = true

  lifecycle_rule {
    condition {
      age = 1
    }
    action {
      type = "AbortIncompleteMultipartUpload"
    }
  }
}

resource "google_bigquery_dataset" "bb200_dataset" {
  dataset_id    = var.bq_dataset_name
  location      = var.location
  delete_contents_on_destroy = true
}

resource "google_dataproc_cluster" "bb200_cluster" {
  name          = var.dp_cluster_name
  region        = var.region

  master_config {
    num_instances = 1
    machine_type  = "n1-standard-4"
  }

  worker_config {
    num_instances = 2
    machine_type  = "n1-standard-4"
  }

  lifecycle {
    ignore_changes = [
      worker_config[0].num_instances,
      worker_config[1].num_instances
    ]
  }
}