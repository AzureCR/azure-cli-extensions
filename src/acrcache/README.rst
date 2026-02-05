Microsoft Azure CLI 'acrcache' Extension
========================================

Overview
--------

The ``acrcache`` extension adds support for managing Azure Container Registry (ACR) cache rules via the Azure CLI.

Features
--------

- Create, update, list, show, delete, and sync cache rules for ACR
- Support for both PassiveSync (pull-through cache) and ActiveSync (proactive synchronization) modes
- Flexible tag filtering with pattern-based and exact match options
- Managed identity authentication for secure cross-registry access
- Comprehensive artifact and platform filtering capabilities

Commands
--------

- ``az acr cache create``: Create a new cache rule
- ``az acr cache update``: Update an existing cache rule
- ``az acr cache list``: List all cache rules in a registry
- ``az acr cache show``: Show details of a specific cache rule
- ``az acr cache delete``: Delete a cache rule
- ``az acr cache sync``: Manually sync a specific tag through an existing cache rule

Parameters
----------

Common Parameters
~~~~~~~~~~~~~~~~~

- ``--registry, -r``: The name of the container registry (required)
- ``--name, -n``: The name of the cache rule (required for most commands)

Cache Rule Creation & Updates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Required Parameters** (create only):

- ``--source-repo, -s``: The full source repository path (e.g., ``docker.io/library/ubuntu``)
- ``--target-repo, -t``: The target repository namespace (e.g., ``ubuntu``)

**Authentication & Identity**:

- ``--cred-set, -c``: The name of the credential set for source registry authentication
- ``--assign-identity, -i``: Resource ID of user-assigned managed identity for cross-registry authentication
- ``--remove-cred-set``: Remove credential set from cache rule (update only, boolean flag)

**Sync Configuration**:

- ``--sync``: Synchronization mode

  - ``passivesync`` (default): Pull-through cache - images cached on demand when pulled
  - ``activesync``: Proactive sync - images automatically synchronized from source every 12 hours

- ``--sync-referrers``: Enable/disable syncing of artifact referrers (requires ``--sync activesync``)

  - ``enabled``: Sync referrers
  - ``disabled`` (default): Do not sync referrers

**Tag Filtering** (requires ``--sync activesync``):

*New Parameters* (preferred):

- ``--tag-equals``: Only sync artifacts with this exact tag name
- ``--tag-starts-with``: Only sync tags that start with the specified string
- ``--tag-ends-with``: Only sync tags that end with the specified string
- ``--tag-contains``: Only sync tags that contain the specified string

*Legacy Parameters* (deprecated - shows warning):

- ``--tag``: Only sync artifacts with this exact tag name
- ``--starts-with``: Only sync tags that start with the specified string
- ``--ends-with``: Only sync tags that end with the specified string
- ``--contains``: Only sync tags that contain the specified string

**Platform & Artifact Filtering** (requires ``--sync activesync``):

- ``--platforms``: Comma-separated list of platforms (e.g., ``linux/amd64,linux/arm64,windows/amd64``)
- ``--include-artifact-types``: Comma-separated list of artifact types to include (mutually exclusive with ``--exclude-artifact-types``)
- ``--exclude-artifact-types``: Comma-separated list of artifact types to exclude (mutually exclusive with ``--include-artifact-types``)
- ``--include-image-types``: Comma-separated list of image types to include (mutually exclusive with ``--exclude-image-types``)
- ``--exclude-image-types``: Comma-separated list of image types to exclude (mutually exclusive with ``--include-image-types``)

**Execution Control**:

- ``--dry-run``: Show what would be synced without creating the rule (create only, requires ``--sync activesync``)
- ``--yes, -y``: Do not prompt for confirmation

Manual Sync Parameters
~~~~~~~~~~~~~~~~~~~~~~

- ``--tag``: The name of the tag to sync immediately (requires existing cache rule with artifact sync enabled)

Installation
------------

Prerequisites
~~~~~~~~~~~~~

1. Install Python 3.6+ (Python 3.12 recommended) from http://python.org

2. Fork and clone the required repositories:

   - Azure CLI: https://github.com/Azure/azure-cli
   - Azure CLI Extensions: https://github.com/AzureCR/azure-cli-extensions

3. Set up the ``azure-cli`` repository::

       git clone https://github.com/<your-github-name>/azure-cli.git
       cd azure-cli
       git remote add upstream https://github.com/Azure/azure-cli.git
       git fetch upstream
       git branch dev --set-upstream-to upstream/dev
       git checkout -b <feature_branch>

   For ``azure-cli-extensions``, follow the same steps but use ``main`` instead of ``dev``::

       git branch main --set-upstream-to upstream/main

   .. note::

      The ACR cache extension is in the ``feature/acrcache`` branch of the ``azure-cli-extensions`` repository. Do NOT merge changes into main.

4. Create and activate a virtual environment::

       python -m venv .venv

   - Windows CMD: ``.venv\Scripts\activate.bat``
   - Windows PowerShell: ``.venv\Scripts\activate.ps1``
   - OSX/Linux (bash): ``source .venv/bin/activate``

5. Install required packages::

       python -m pip install -U pip
       pip install setuptools==70.0.0
       pip install --force-reinstall wheel==0.30.0
       pip install -U azdev
       azdev setup -c -r azure-cli-extensions/

   .. note::

      Due to a known issue (https://github.com/Azure/azure-cli/issues/29467), Azure CLI requires setuptools 70.0.0 and wheel 0.30.0.

6. Build the extension::

       azdev extension build acrcache

Development
-----------

- Document customer-facing changes in ``HISTORY.rst``
- Update the version in ``setup.py`` for new releases
- After making changes, rebuild and reinstall::

      azdev extension build acrcache
      az extension remove --name acrcache
      az extension add --source "path/dist/acrcache.whl"

Usage Examples
--------------

Basic Cache Rules
~~~~~~~~~~~~~~~~~

Create a basic pull-through cache rule::

    az acr cache create -r myregistry -n my-cache-rule \
      -s docker.io/library/nginx -t nginx

Create an active sync rule with tag filtering::

    az acr cache create -r myregistry -n sync-rule \
      -s docker.io/library/alpine -t alpine \
      --sync activesync --tag-starts-with 3.1

Advanced Filtering
~~~~~~~~~~~~~~~~~~

Create cache rule with platform and artifact filtering::

    az acr cache create -r myregistry -n filtered-rule \
      -s docker.io/library/redis -t redis \
      --sync activesync --platforms linux/amd64,linux/arm64 \
      --tag-contains slim

Authentication Methods
~~~~~~~~~~~~~~~~~~~~~~

**User-Assigned Managed Identity**:

Use ``--assign-identity`` for secure ACR-to-ACR caching within the same tenant::

    az acr cache create -r targetregistry -n acr-rule \
      -s sourceregistry.azurecr.io/myapp -t myapp \
      --assign-identity /subscriptions/<sub-id>/resourceGroups/<rg>/providers/Microsoft.ManagedIdentity/userAssignedIdentities/<identity-name>

**Credential Set**:

Use ``--cred-set`` for credential-based authentication::

    az acr cache create -r myregistry -n my-rule \
      -s docker.io/library/nginx -t nginx \
      --cred-set my-credential-set

Cache Rule Management
~~~~~~~~~~~~~~~~~~~~~

List all cache rules::

    az acr cache list -r myregistry

Update cache rule with new filters::

    az acr cache update -r myregistry -n my-rule \
      --tag-ends-with -alpine --sync-referrers enabled

Manually sync a specific tag::

    az acr cache sync -r myregistry -n my-rule --tag latest

Delete a cache rule::

    az acr cache delete -r myregistry -n my-rule

Important Notes
---------------

Sync Modes
~~~~~~~~~~

- **PassiveSync** (default): Pull-through cache - images are cached when first pulled
- **ActiveSync**: Proactive synchronization - images are automatically pulled every 12 hours

Parameter Constraints
~~~~~~~~~~~~~~~~~~~~~

- ``--sync-referrers enabled`` requires ``--sync activesync``
- All filtering parameters (platforms, artifacts, tags) require ``--sync activesync``
- Tag filtering is mutually exclusive: use either exact match OR pattern-based filters
- Include/exclude parameters are mutually exclusive within the same type
- Source repository path cannot contain tags (use tag filtering parameters instead)

Legacy Parameter Migration
~~~~~~~~~~~~~~~~~~~~~~~~~~

Legacy tag filtering parameters show deprecation warnings. Use the new explicit parameters for clarity:

==============================  ==============================
Legacy Parameter                New Parameter
==============================  ==============================
``--tag``                       ``--tag-equals``
``--starts-with``               ``--tag-starts-with``
``--ends-with``                 ``--tag-ends-with``
``--contains``                  ``--tag-contains``
==============================  ==============================

Requirements
------------

- Azure CLI version **2.55.0** or higher

Check your version with::

    az version

For more details, see the `Azure CLI documentation <https://learn.microsoft.com/cli/azure/acr>`_.
