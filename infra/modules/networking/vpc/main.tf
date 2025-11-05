module "vpc" {
    source = "terraform-aws-modules/vpc/aws"
    version = "5.8.1"

    name = var.vpc_name
    cidr = var.cidr
    azs = ["us-west-1"]

    private_subnets = var.private_subnets
    public_subnets = var.public_subnet

    enable_nat_gateway = var.nat_gateway
    single_nat_gateway = var.single_nat
    enable_dns_hostnames = true #hard coded as likely will always use

    private_subnet_tags = var.private_subnets_tags
    public_subnet_tags = var.public_subnet_tags
}