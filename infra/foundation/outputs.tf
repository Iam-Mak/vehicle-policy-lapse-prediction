output "resource_group_name" {
  description = "Azure Resource Group name"
  value       = azurerm_resource_group.main.name
}

output "container_app_environment_id" {
  description = "Azure Container Apps Environment ID"
  value       = azurerm_container_app_environment.main.id
}

output "acr_login_server" {
  description = "Azure Container Registry login server"
  value       = azurerm_container_registry.main.login_server
}

output "acr_username" {
  description = "Azure Container Registry admin username"
  value       = azurerm_container_registry.main.admin_username
}

output "acr_password" {
  description = "Azure Container Registry admin password"

  value     = azurerm_container_registry.main.admin_password
  sensitive = true
}