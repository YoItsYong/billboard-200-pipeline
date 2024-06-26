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