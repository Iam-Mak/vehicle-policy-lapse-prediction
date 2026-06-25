output "model_service_url" {
  description = "Model Service URL"
  value       = azurerm_container_app.model_service.latest_revision_fqdn
}

output "api_gateway_url" {
  description = "API Gateway URL"
  value       = azurerm_container_app.api_gateway.latest_revision_fqdn
}