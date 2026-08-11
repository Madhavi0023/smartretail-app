
# ============================================================
# EKS CLUSTER
# ============================================================

resource "aws_eks_cluster" "main" {
  name     = "${var.project_name}-eks"
  role_arn = aws_iam_role.eks_cluster.arn
  access_config {

    authentication_mode = "API_AND_CONFIG_MAP"

  }

  vpc_config {
    subnet_ids = aws_subnet.private[*].id

    endpoint_private_access = true
    endpoint_public_access  = true
  }

  tags = {
    Name        = "${var.project_name}-eks"
    Environment = var.environment
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_cluster_policy
  ]
}


# ============================================================
# EKS MANAGED NODE GROUP
# ============================================================

resource "aws_eks_node_group" "main" {
  cluster_name    = aws_eks_cluster.main.name
  node_group_name = "${var.project_name}-node-group"
  node_role_arn   = aws_iam_role.eks_node.arn

  subnet_ids = aws_subnet.private[*].id

  instance_types = ["t3.medium"]

  scaling_config {
    desired_size = 2
    min_size     = 1
    max_size     = 3
  }

  tags = {
    Name        = "${var.project_name}-node"
    Environment = var.environment
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks_worker_node_policy,
    aws_iam_role_policy_attachment.eks_cni_policy,
    aws_iam_role_policy_attachment.ecr_read_only_policy
  ]
}


# ============================================================
# EKS OIDC TLS CERTIFICATE
# ============================================================

data "tls_certificate" "eks" {
  url = aws_eks_cluster.main.identity[0].oidc[0].issuer
}


# ============================================================
# EKS OIDC PROVIDER
# ============================================================

resource "aws_iam_openid_connect_provider" "eks" {
  client_id_list = [
    "sts.amazonaws.com"
  ]

  thumbprint_list = [
    data.tls_certificate.eks.certificates[0].sha1_fingerprint
  ]

  url = aws_eks_cluster.main.identity[0].oidc[0].issuer
}
resource "aws_eks_access_entry" "github_actions" {

  cluster_name = aws_eks_cluster.main.name

  principal_arn = data.aws_iam_role.github_actions.arn

  type = "STANDARD"

}
resource "aws_eks_access_policy_association" "github_actions" {

  cluster_name = aws_eks_cluster.main.name

  principal_arn = data.aws_iam_role.github_actions.arn

  policy_arn = "arn:aws:eks::aws:cluster-access-policy/AmazonEKSClusterAdminPolicy"

  access_scope {

    type = "cluster"

  }

}
