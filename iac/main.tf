variable "users" {
    type = set(string)
}

data "azurerm_cosmosdb_account" "account" {
    name = "ka-training-drj-serverless"
    resource_group_name = "free_cosmos"
}

data "azurerm_cosmosdb_sql_database" "database" {
    name = "company_data"
    resource_group_name = "free_cosmos"
    account_name = "ka-training-drj-serverless"
}

provider "azurerm" {
    features {
      
    }
}

resource "azurerm_cosmosdb_sql_container" "company_container" {
    for_each = var.users
    name = "company_${each.value}"
    account_name = data.azurerm_cosmosdb_account.account.name
    database_name = data.azurerm_cosmosdb_sql_database.database.name
    resource_group_name = "free_cosmos"
    partition_key_path = "/id"

}

resource "azurerm_cosmosdb_sql_container" "department_container" {
    for_each = var.users
    name = "department_${each.value}"
    account_name = data.azurerm_cosmosdb_account.account.name
    database_name = data.azurerm_cosmosdb_sql_database.database.name
    resource_group_name = "free_cosmos"
    partition_key_path = "/id"

}

resource "azurerm_cosmosdb_sql_container" "employee_container" {
    for_each = var.users
    name = "employee_${each.value}"
    account_name = data.azurerm_cosmosdb_account.account.name
    database_name = data.azurerm_cosmosdb_sql_database.database.name
    resource_group_name = "free_cosmos"
    partition_key_path = "/id"

}