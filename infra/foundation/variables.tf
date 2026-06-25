variable "resource_group_name" {
  description = "Azure Resource Group name"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
}

variable "log_analytics_name" {
  description = "Log Analytics Workspace name"
  type        = string
}

variable "acr_name" {
  description = "Azure Container Registry name"
  type        = string
}

variable "container_app_env_name" {
  description = "Azure Container Apps Environment name"
  type        = string
}