locals {
  common_tags = {
    Project     = "vehicle-policy-lapse"
    Environment = "dev"
    ManagedBy   = "Terraform"
  }

  model_service_name = "model-service"
  api_gateway_name   = "api-gateway"
}