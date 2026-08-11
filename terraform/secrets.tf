resource "aws_secretsmanager_secret" "smartretail_db" {
  name = "${var.project_name}/database"

  description = "SmartRetail PostgreSQL database credentials"

  tags = {
    Name        = "${var.project_name}-database-secret"
    Environment = var.environment
  }
}