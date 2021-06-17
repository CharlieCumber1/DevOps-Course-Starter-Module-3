terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 2.49"
    }
  }
}
provider "azurerm" {
  features {}
}

data "azurerm_resource_group" "main" {
  name = "SoftwirePilot_CharlieCumber_ProjectExercise"
}

resource "azurerm_app_service_plan" "main" {
  name                = "terraformed-asp"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  kind                = "Linux"
  reserved            = true
  sku {
    tier = "Basic"
    size = "B1"
  }
}

resource "azurerm_cosmosdb_account" "main" {
  name                = "charlie-devops-cosmosdb-account"
  resource_group_name = data.azurerm_resource_group.main.name
  kind                = "MongoDB"
  location            = data.azurerm_resource_group.main.location
  geo_location {
    location          = data.azurerm_resource_group.main.location
    failover_priority = 0
  }
  consistency_policy {
    consistency_level = "Session"
  }
  offer_type = "Standard"
  capabilities {
    name = "EnableServerless"
  }
  capabilities {
    name = "EnableMongo"
  }
  lifecycle {
    prevent_destroy = true
  }
}

resource "azurerm_cosmosdb_mongo_database" "main" {
  name                = "charlie-devops-cosmos-mongo-db"
  resource_group_name = data.azurerm_resource_group.main.name
  account_name        = azurerm_cosmosdb_account.main.name
}

resource "azurerm_app_service" "main" {
  name                = "charlie-devops-to-do-terraform"
  location            = data.azurerm_resource_group.main.location
  resource_group_name = data.azurerm_resource_group.main.name
  app_service_plan_id = azurerm_app_service_plan.main.id
  site_config {
    app_command_line = ""
    linux_fx_version = "DOCKER|charliecumber/todo-app:latest"
  }
  app_settings = {
    "DOCKER_REGISTRY_SERVER_URL" = "https://index.docker.io"
    "MONGODB_CONNECTION_STRING"  = "mongodb://${azurerm_cosmosdb_account.main.name}:${azurerm_cosmosdb_account.main.primary_key}@${azurerm_cosmosdb_account.main.name}.mongo.cosmos.azure.com:10255"
  }
}
