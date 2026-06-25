resource "azurerm_resource_group" "main" {
  name     = var.resource_group_name
  location = var.location

  tags = local.common_tags
}

resource "azurerm_log_analytics_workspace" "main" {
  name                = var.log_analytics_name
  location            = var.location
  resource_group_name = azurerm_resource_group.main.name

  sku               = "PerGB2018"
  retention_in_days = 30

  tags = local.common_tags
}

resource "azurerm_container_registry" "main" {
  name                = var.acr_name
  resource_group_name = azurerm_resource_group.main.name
  location            = var.location

  sku           = "Basic"
  admin_enabled = true

  tags = local.common_tags
}

resource "azurerm_container_app_environment" "main" {
  name                       = var.container_app_env_name
  location                   = var.location
  resource_group_name        = azurerm_resource_group.main.name
  log_analytics_workspace_id = azurerm_log_analytics_workspace.main.id

  tags = local.common_tags
}