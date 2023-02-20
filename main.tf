terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.16.0"
    }
  }
}

provider "google" {
  credentials = file("${var.credential_path}")
  project     = var.project_id
  region      = "asia-northeast1"
  zone        = "asia-northeast1-a"
}

resource "google_project_iam_member" "secret_manager" {
  project = var.project_id
  role    = "roles/secretmanager.secretAccessor"
  member  = "serviceAccount:${var.project_id}@appspot.gserviceaccount.com"
}

resource "google_secret_manager_secret" "secret_mail" {
  secret_id = "secret_mail"
  lifecycle {
    prevent_destroy = true
  }
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret" "secret_password" {
  secret_id = "secret_password"
  lifecycle {
    prevent_destroy = true
  }
  replication {
    automatic = true
  }
}

resource "google_secret_manager_secret_version" "secret_mail" {
  secret      = google_secret_manager_secret.secret_mail.id
  secret_data = var.jobcan_email
}

resource "google_secret_manager_secret_version" "secret_password" {
  secret      = google_secret_manager_secret.secret_password.id
  secret_data = var.jobcan_password
}

data "archive_file" "function_archive" {
  type        = "zip"
  source_dir  = "./src"
  output_path = "./src.zip"
}

resource "google_storage_bucket" "bucket" {
  name          = "bucket-jobcan-auto"
  location      = "asia-northeast1"
  storage_class = "STANDARD"
}

resource "google_storage_bucket_object" "packages" {
  name   = "packages/functions.${data.archive_file.function_archive.output_md5}.zip"
  bucket = google_storage_bucket.bucket.name
  source = data.archive_file.function_archive.output_path
}

resource "google_cloudfunctions_function" "function" {
  name                  = "function-jobcan-auto"
  runtime               = "python37"
  source_archive_bucket = google_storage_bucket.bucket.name
  source_archive_object = google_storage_bucket_object.packages.name
  available_memory_mb   = 512
  timeout               = 540
  event_trigger {
    event_type = "providers/cloud.pubsub/eventTypes/topic.publish"
    resource   = google_pubsub_topic.topic.id
  }
  environment_variables = {
    PROJECT_ID = "${var.project_number}"
  }
  entry_point = "main"
}

resource "google_pubsub_topic" "topic" {
  name = "topic-jobcan-auto"
}

resource "google_cloud_scheduler_job" "jobcan-auto-scheduler" {
  name      = "jobcan-auto-scheduler"
  project   = var.project_id
  schedule  = "${var.cron}" // 例: 平日の9時、12時、13時、18時に実行 → 0 9,12,13,17 * * 1,2,3,4,5
  time_zone = "Asia/Tokyo"

  pubsub_target {
    topic_name = "projects/${var.project_id}/topics/topic-jobcan-auto"
    data       = base64encode("jobcan-auto")
  }
}