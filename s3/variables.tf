variable "bucket_name" {
  description = "Name of the bucket where the csv files will be stored"
  type = string
  default = "bucket-by-tf"
}

variable "project_name" {
    default = "Headlines newsletter"
}