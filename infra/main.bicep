targetScope = 'resourceGroup'

@description('Base name for resources. Keep short and unique in the resource group.')
param baseName string = 'skillfirst'

@description('Azure region.')
param location string = resourceGroup().location

@description('Container image, e.g. <registry>.azurecr.io/skill-first-ai:1.0.0')
param containerImage string = 'acrmiqsfai26.azurecr.io/skill-first-ai:1.0.1'

@description('Existing Azure Container Registry name that hosts the image.')
param acrName string = 'acrmiqsfai26'

@description('APIM subscription key header name exposed to the Foundry agent.')
param mcpSubscriptionHeader string = 'x-api-key'

module foundry './foundry.bicep' = {
  name: 'skillFirstFoundryInfra'
  params: {
    baseName: baseName
    location: location
    containerImage: containerImage
    acrName: acrName
    mcpSubscriptionHeader: mcpSubscriptionHeader
  }
}

output mcpUrl string = foundry.outputs.mcpUrl
output apimGatewayUrl string = foundry.outputs.apimGatewayUrl
output subscriptionHeader string = foundry.outputs.subscriptionHeader
output createdResourceNames object = foundry.outputs.createdResourceNames
