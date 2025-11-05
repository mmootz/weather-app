variable "vpc_name" {
    description = "Name of vpc used for cluster"
    type = string
}

variable "cidr" {
    description = "cidr of the network eg 10.0.1.0/24"
    type = string
}

variable "private_subnets" {
    description = "list of the private subnets for this cluster"
    type = list
}

variable "public_subnet" {
  description = "list of the public subnets for this cluster"
  type = list
}

variable "nat_gateway" {
    description = "enable the nat gateway"
    type = bool
}

variable "single_nat" {
    description = "enable single nat"
    type = bool
}

variable "public_subnet_tags" {
  description = "tags for the public subnet"
  type = map(string)
}

variable "private_subnets_tags" {
  description = "tags for the private subnet"
  type = map(string)
}