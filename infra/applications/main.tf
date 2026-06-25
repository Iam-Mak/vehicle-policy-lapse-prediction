resource "azurerm_container_app" "model_service" {
  name                         = var.container_app_name
  resource_group_name          = data.terraform_remote_state.foundation.outputs.resource_group_name
  container_app_environment_id = data.terraform_remote_state.foundation.outputs.container_app_environment_id

  revision_mode = "Single"

  template {
    container {
      name  = "model-service"
      image = "${data.terraform_remote_state.foundation.outputs.acr_login_server}/${var.model_service_image}"

      cpu    = 0.5
      memory = "1Gi"
    }
  }

  ingress {
    external_enabled = true
    target_port      = 8001

    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  registry {
    server               = data.terraform_remote_state.foundation.outputs.acr_login_server
    username             = data.terraform_remote_state.foundation.outputs.acr_username
    password_secret_name = "acr-password"
  }

  secret {
    name  = "acr-password"
    value = data.terraform_remote_state.foundation.outputs.acr_password
  }
}

resource "azurerm_container_app" "api_gateway" {
  name                         = var.api_gateway_name
  resource_group_name          = data.terraform_remote_state.foundation.outputs.resource_group_name
  container_app_environment_id = data.terraform_remote_state.foundation.outputs.container_app_environment_id

  revision_mode = "Single"

  template {
    container {
      name  = "api-gateway"
      image = "${data.terraform_remote_state.foundation.outputs.acr_login_server}/${var.api_gateway_image}"

      cpu    = 0.5
      memory = "1Gi"

      env {
        name  = "MODEL_SERVICE_URL"
        value = "https://${azurerm_container_app.model_service.latest_revision_fqdn}/api/v1/infer"
      }
    }
  }

  ingress {
    external_enabled = true
    target_port      = 5000

    traffic_weight {
      latest_revision = true
      percentage      = 100
    }
  }

  registry {
    server               = data.terraform_remote_state.foundation.outputs.acr_login_server
    username             = data.terraform_remote_state.foundation.outputs.acr_username
    password_secret_name = "acr-password"
  }

  secret {
    name  = "acr-password"
    value = data.terraform_remote_state.foundation.outputs.acr_password
  }
}