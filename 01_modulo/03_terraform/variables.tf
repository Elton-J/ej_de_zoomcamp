variable "project" {
  description = "Project"
  default     = "de-zoom-421502"
}

variable "location" {
  description = "Project location"
  default     = "US"
}

variable "region" {
  description = "Region"
  default     = "us-central1"
}


variable "credentials" {
  description = "Credentials path"
  default     = "C:/Users/elton.junior_amaris/Desktop/ej_de_zoomcamp/01_modulo/03_terraform/keys/de-zoom-421502-b2b4433f8755.json"
}



variable "bq_dataset_name" {
  description = "Nome do dataset no BigQuery"
  default     = "dataset_exemplo"

}

variable "gcs_bucket_name" {
  description = "Nome do bucket no Google Cloud Storage"
  default     = "de-zoom-421502-terraform-bucket"

}