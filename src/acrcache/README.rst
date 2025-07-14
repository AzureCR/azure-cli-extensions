Microsoft Azure CLI 'acrcache' Extension
==========================================

# Microsoft Azure CLI 'acrcache' Extension

## Overview

The `acrcache` extension adds support for managing Azure Container Registry (ACR) cache rules via the Azure CLI. Cache rules allow you to automate artifact synchronization, apply filters, and optimize image retrieval for your container workloads.

## Features

- Create, update, list, show, and delete cache rules for ACR.
- Configure artifact sync with flexible filters:
  - **--platforms**: Filter which platforms to sync (e.g., `linux/amd64`, `linux/arm64`).
  - **--sync-referrers**: Enable or disable syncing of referrers.
  - **--include-artifact-types**: Specify artifact types to include in sync.
  - **--exclude-artifact-types**: Specify artifact types to exclude from sync.
- Support for credential sets and tag filtering.

## Installation

You can install the extension using the Azure CLI:

```sh
az extension add --name acrcache
```

## Usage

### List cache rules

```sh
az acr cache list -r <registry-name>
```

### Create a cache rule

```sh
az acr cache create -r <registry-name> -n <rule-name> -s <source-repo> -t <target-repo> \
  --sync true --platforms linux/amd64,linux/arm64 --sync-referrers enabled \
  --include-artifact-types images,notary-project-signature
```

### Update a cache rule

```sh
az acr cache update -r <registry-name> -n <rule-name> --platforms linux/amd64
```

### Show a cache rule

```sh
az acr cache show -r <registry-name> -n <rule-name>
```

### Delete a cache rule

```sh
az acr cache delete -r <registry-name> -n <rule-name>
```

## Minimum Azure CLI Version

This extension requires Azure CLI version **2.57.0** or higher.

## Documentation

For more details, see the official [Azure CLI documentation](https://docs.microsoft.com/cli/azure/acr).


This package is for the 'acrcache' extension to support the Azure Container Registry cache rules.

