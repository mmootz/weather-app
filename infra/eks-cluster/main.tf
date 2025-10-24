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



 vpc_id     = aws_vpc.main.id

 subnet_ids = aws_subnet.public_subnet.*.id



 tags = {

   Environment = "dev"

   Terraform   = "true"

 }

}
