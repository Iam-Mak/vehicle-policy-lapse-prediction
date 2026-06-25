variable "resource_group_name" {
  description = "Terraform state resource group"
  type        = string
}

variable "location" {
  description = "Azure region"
  type        = string
}

variable "storage_account_name" {
  description = "Terraform state storage account"
  type        = string
}

variable "container_name" {
  description = "Terraform state container"
  type        = string
}