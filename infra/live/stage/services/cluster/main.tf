terraform {
  required_version = ">= 1.0.0, < 2.0.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
    region = "us-west-1"
}

module "stage_cluster" {
    source = "../../../../modules/eks-cluster"

    name = var.cluster_name
    min_size = var.min_size
    max_size = var.max_size
    desired_size = var.desired_size
    node_group_instance_types = var.node_group_instance_types

}