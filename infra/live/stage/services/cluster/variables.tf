variable "cluster_name" {
  description = "name of the cluster"
  type = string
  default = "staging-cluster"
}

variable "min_size" {
    description = "min size of cluster"
    type = number
    default = 1
}

variable "max_size" {
    description = "max size of cluster"
    type = number
    default = 3
}

variable "node_group_instance_types" {
    description = "list of instance types to use"
    type = list 
    default = ["t3.small"]
}

variable "desired_size" {
    description = "normal size of cluster"
    type = number
    default = 2
}

variable "remote_state_bucket" {
  description = "remote bucket for staging"
  type = string
  default = "mmootz-weather-app-staging"
}

variable "remote_state_key" {
  description = "remote bucket key"
  type = string
  default = "global/s3/stage/terraform.tfstate"
}