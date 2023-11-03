terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.16"
    }
  }

  required_version = ">= 1.2.0"
}

provider "aws" {
  region = "eu-central-1"
}

module "iam" {
  source = "./iam"
}

module "s3" {
  source = "./s3"
}

module "lambda" {
  source = "./lambda"

  lambda_role_arn = module.iam.lambda_role_arn
}

module "event_bridge" {
  source = "./event_bridge"

  lambda_arn = module.lambda.lambda_arn
}