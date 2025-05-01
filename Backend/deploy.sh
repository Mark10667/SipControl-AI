#!/bin/bash

# Deploy to Azure Web App
echo "Deploying to Azure Web App..."

# Install Azure CLI if not already installed
if ! command -v az &> /dev/null; then
    echo "Azure CLI not found. Installing..."
    curl -sL https://aka.ms/InstallAzureCLIDeb | sudo bash
fi

# Login to Azure
echo "Logging in to Azure..."
az login

RESOURCE_GROUP="hackthon-drinking-agent"
WEBAPP_NAME="drinkingwebapp"

# Configure environment variables
echo "Configuring environment variables..."
az webapp config appsettings set --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP --settings \
    MONGODB_URI="$MONGODB_URI" \
    MONGODB_DATABASE="$MONGODB_DATABASE" \
    BLOB_CONNECTION_STRING="$BLOB_CONNECTION_STRING" \
    BLOB_CONTAINER_NAME="$BLOB_CONTAINER_NAME" \
    AZURE_ENDPOINT="$AZURE_ENDPOINT" \
    AZURE_API_KEY="$AZURE_API_KEY" \
    GPT4_DEPLOYMENT="$GPT4_DEPLOYMENT" \
    API_VERSION="$API_VERSION"

# Deploy the application
echo "Deploying the application..."
az webapp deployment source config-local-git --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP

# Get the deployment URL
DEPLOY_URL=$(az webapp deployment list-publishing-profiles --name $WEBAPP_NAME --resource-group $RESOURCE_GROUP --query "[?publishMethod=='MSDeploy'].publishUrl" -o tsv)

echo "Deployment URL: $DEPLOY_URL"
echo "Deployment completed successfully!" 