
# ============================================================
# RDS SUBNET GROUP
# ============================================================

resource "aws_db_subnet_group" "main" {
  name = "${var.project_name}-db-subnet-group"

  subnet_ids = aws_subnet.private[*].id

  tags = {
    Name        = "${var.project_name}-db-subnet-group"
    Environment = var.environment
  }
}


# ============================================================
# POSTGRESQL RDS INSTANCE
# ============================================================

resource "aws_db_instance" "postgres" {
  identifier = "${var.project_name}-postgres"

  # Database Engine
  engine         = "postgres"
  engine_version = "16"

  # Instance
  instance_class = "db.t3.micro"

  # Storage
  allocated_storage     = 20
  max_allocated_storage = 50
  storage_type          = "gp3"
  storage_encrypted     = true

  # Database Credentials
  db_name  = var.db_name
  username = var.db_username
  password = var.db_password

  # Networking
  db_subnet_group_name = aws_db_subnet_group.main.name

  vpc_security_group_ids = [
    aws_security_group.rds.id
  ]

  publicly_accessible = false

  # Backup
  backup_retention_period = 7
  backup_window           = "03:00-04:00"

  # Maintenance
  maintenance_window = "sun:04:00-sun:05:00"

  # Dev/Learning Environment
  skip_final_snapshot = true
  deletion_protection = false

  tags = {
    Name        = "${var.project_name}-postgres"
    Environment = var.environment
  }
}

