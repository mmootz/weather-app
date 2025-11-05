terraform {
  backend "s3" {
    bucket = "mmootz-weather-app-staging"
    key = "global/s3/stage/terraform.tfstate"
    region = "us-west-1"
  }
}