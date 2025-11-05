module "vpc" {
  source = "../networking/vpc"
   
   vpc_name =  "${var.name}-eks-vpc"
   
   cidr = "10.0.0.0/16"
   private_subnets = ["10.0.1.0/24", "10.0.2.0/24", "10.0.3.0/24"]
   private_subnets_tags = { "private_vpc" = "${var.name}-eks-private-vpc" }

   public_subnet = ["10.0.4.0/24","10.0.5.0/24","10.0.6.0/24"]
   public_subnet_tags = { "public_vpc" = "${var.name}-eks-public-vpc" }

   nat_gateway = true
   single_nat = true

}


module "eks" {

 source  = "terraform-aws-modules/eks/aws"

 version = "~> 20.31"

 cluster_name    = var.name

 cluster_version = var.k8s_version

 cluster_endpoint_public_access = true

 enable_cluster_creator_admin_permissions = true

 eks_managed_node_groups = {

   example = {

     instance_types = var.node_group_instance_types

     min_size       = var.min_size

     max_size       = var.max_size

     desired_size   = var.desired_size

   }

 }

vpc_id = module.vpc.vpc_id
subnet_ids = module.vpc.private_subnets

 tags = merge(
   var.custom_tags,
   {
     key = "name",
     value = var.name
     Terraform = "true"
   }
)

}
