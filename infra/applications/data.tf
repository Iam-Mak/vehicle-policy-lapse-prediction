data "terraform_remote_state" "foundation" {
  backend = "azurerm"

  config = {
    resource_group_name  = "terraform-state-rg"
    storage_account_name = "vehiclelapsetfstate12345"
    container_name       = "tfstate"
    key                  = "foundation.tfstate"
  }
}