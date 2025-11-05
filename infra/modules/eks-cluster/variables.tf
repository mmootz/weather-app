variable "name" {
    description = "name of cluster"
    type = string

    # validation {
    #   condition = var.name == 
    #   error_message = "Cluster name can not be blank"
    # }
}

variable "k8s_version" {
    description = "k8s version"
    type = number
    default = 1.33

    validation {
      condition = var.k8s_version > 0
      error_message = "k8s_version can't be blank"
    }
    validation {
      condition = var.k8s_version >= 1.28
      error_message = "K8s version to low not supported by eks"
    }

    validation {
      condition = var.k8s_version <= 1.40
      error_message = "K8s version too high not supported by eks yet"
    }

}

variable "node_group_instance_types" {
    description = "list of instance types to use"
    type = list
}

variable "min_size" {
    description = "Minium size of the nodes in cluster"
    type = number

    validation {
      condition = var.min_size > 0
      error_message = "min_size can't be zero"
    }

    validation {
      condition = var.min_size <= 10
      error_message = "min_size can't be over 10 for costs"
    }
}

variable "max_size" {
    description = "Maximum size of nodes in cluster"
    type = number

    validation {
      condition = var.max_size > 0
      error_message = "Max size can't be zero"
    }

    validation {
      condition = var.max_size <= 10
      error_message = "Max size can't be over 10 for costs"
    }
}

variable "desired_size" {
    description = "desired size of nodes in cluster"
    type = number


    validation {
      condition = var.desired_size > 0
      error_message = "desired_size can't be zero"
    }

    validation {
      condition = var.desired_size <= 10
      error_message = "desired_size can't be over 10 for costs"
    }
}
variable "custom_tags" {
    description = "Custom tags to add to the cluster"
    type = map(string)
    default = {}
  
}