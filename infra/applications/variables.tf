variable "container_app_name" {
  description = "Model Service Container App name"
  type        = string
}

variable "api_gateway_name" {
  description = "API Gateway Container App name"
  type        = string
}

variable "model_service_image" {
  description = "Model Service Docker image"
  type        = string
}

variable "api_gateway_image" {
  description = "API Gateway Docker image"
  type        = string
}