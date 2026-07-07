// Minimal Bicep for the skill-first MCP server.
//
// Scope: one Container App Environment, one Container App running the
// uvicorn MCP server, one APIM AI Gateway with the Container App
// registered as an MCP source.
//
// Not included: the Foundry project itself (use the existing one) or
// any storage (this demo is stateless).

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

var envName = '${baseName}-env'
var appName = '${baseName}-mcp'
var lawName = '${baseName}-law'
var apimName = '${baseName}-apim'
var uamiName = '${baseName}-uami'
var acrPullRoleDefinitionId = subscriptionResourceId('Microsoft.Authorization/roleDefinitions', '7f951dda-4ed3-4680-a7ca-43fe172d538d')

resource acr 'Microsoft.ContainerRegistry/registries@2023-11-01-preview' existing = {
  name: acrName
}

resource law 'Microsoft.OperationalInsights/workspaces@2023-09-01' = {
  name: lawName
  location: location
  properties: {
    retentionInDays: 30
    sku: {
      name: 'PerGB2018'
    }
  }
}

resource env 'Microsoft.App/managedEnvironments@2024-03-01' = {
  name: envName
  location: location
  properties: {
    appLogsConfiguration: {
      destination: 'log-analytics'
      logAnalyticsConfiguration: {
        customerId: law.properties.customerId
        sharedKey: law.listKeys().primarySharedKey
      }
    }
  }
}

resource uami 'Microsoft.ManagedIdentity/userAssignedIdentities@2023-01-31' = {
  name: uamiName
  location: location
}

resource acrPullAssignment 'Microsoft.Authorization/roleAssignments@2022-04-01' = {
  name: guid(acr.id, uami.id, acrPullRoleDefinitionId)
  scope: acr
  properties: {
    roleDefinitionId: acrPullRoleDefinitionId
    principalId: uami.properties.principalId
    principalType: 'ServicePrincipal'
  }
}

resource app 'Microsoft.App/containerApps@2024-03-01' = {
  name: appName
  location: location
  identity: {
    type: 'UserAssigned'
    userAssignedIdentities: {
      '${uami.id}': {}
    }
  }
  properties: {
    managedEnvironmentId: env.id
    configuration: {
      registries: [
        {
          server: acr.properties.loginServer
          identity: uami.id
        }
      ]
      ingress: {
        external: true
        targetPort: 8080
        transport: 'auto'
        // Critical for MCP streaming: do not buffer responses.
        corsPolicy: {
          allowedOrigins: ['*']
          allowedMethods: ['GET', 'POST', 'OPTIONS']
        }
      }
    }
    template: {
      containers: [
        {
          name: 'mcp'
          image: containerImage
          resources: {
            cpu: 1
            memory: '2Gi'
          }
          env: [
            {
              name: 'PORT'
              value: '8080'
            }
          ]
        }
      ]
      scale: {
        minReplicas: 1
        maxReplicas: 3
      }
    }
  }
  dependsOn: [
    acrPullAssignment
  ]
}

resource apim 'Microsoft.ApiManagement/service@2023-09-01-preview' = {
  name: apimName
  location: location
  sku: {
    name: 'Developer'
    capacity: 1
  }
  properties: {
    publisherEmail: 'ops@skill-first.example'
    publisherName: 'Skill-first AI'
  }
}

// The MCP tool registration in APIM AI Gateway is done via the portal
// (Workspaces & Tools -> Add tool -> MCP) because the AI Gateway resource
// types are still preview-only and partial in Bicep. See
// src/skill_first_ai/foundry/deploy.md for the exact steps.

output mcpUrl string = 'https://${app.properties.configuration.ingress.fqdn}/mcp'
output apimGatewayUrl string = apim.properties.gatewayUrl
output subscriptionHeader string = mcpSubscriptionHeader
output createdResourceNames object = {
  logAnalyticsWorkspace: law.name
  containerAppsEnvironment: env.name
  userAssignedIdentity: uami.name
  containerApp: app.name
  apim: apim.name
}
