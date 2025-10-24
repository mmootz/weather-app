variable "name" {
    description = "name of cluster"
    type = string
    default = "eks-cluster"
}

variable "k8s_version" {
    description = "k8s version"
    type = number
    default = 1.33
}

variable "node_group_instance_types" {
    description = "list of instance types to use"
    type = list
    default = ["t3.small"]  
}

variable "min_size" {
    description = "Minium size of the nodes in cluster"
    type = number
    default = 1
  
}

variable "max_size" {
    description = "Maxium size of nodes in cluster"
    type = number
    default = 3
}

variable "desired_size" {
    description = "desired size of nodes in cluster"
    type = number
    default = 2
}