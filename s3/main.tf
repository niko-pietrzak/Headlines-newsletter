resource "aws_s3_bucket" "news_bucket" {
  bucket = var.bucket_name

  tags = {
    Project = var.project_name
    Environment = "Terraform"
  }
}

resource "aws_s3_object" "inputs_folder" {
  bucket = aws_s3_bucket.news_bucket.id
  key    = "inputs/" # Key represents the folder name
}