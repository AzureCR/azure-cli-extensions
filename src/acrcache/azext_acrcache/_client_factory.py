# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------
# pylint: disable=line-too-long
import logging
import traceback
from azure.cli.core._profile import Profile

# Set up logging
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def cf_acrcache(cli_ctx, *_):
    from azure.cli.core.commands.client_factory import get_mgmt_service_client, get_subscription_id
    from azure.cli.core._profile import Profile
    from azext_acrcache.vendored_sdks.containerregistry.v2025_07_01_preview.generated.container_registry_management_client import ContainerRegistryManagementClient
        # Debug logging

    credential = Profile(cli_ctx=cli_ctx).get_login_credentials()[0]
    logger.debug(f"Credential: {credential}")
    subscription_id = get_subscription_id(cli_ctx)
    logger.debug(f"Retrieved Subscription ID: {subscription_id}")
    logger.debug(f"cli_ctx: {cli_ctx}")
    return get_mgmt_service_client(cli_ctx, ContainerRegistryManagementClient, subscription_id=subscription_id).cache_rules

def cf_acrreg(cli_ctx, *_):
    from azure.cli.core.commands.client_factory import get_mgmt_service_client, get_subscription_id
    from azext_acrcache.vendored_sdks.containerregistry.v2025_07_01_preview.generated.container_registry_management_client import ContainerRegistryManagementClient
    
    credential = Profile(cli_ctx=cli_ctx).get_login_credentials()[0]
    logger.debug(f"Credential type: {type(credential)}")
    subscription_id = get_subscription_id(cli_ctx)
    logger.debug(f"Retrieved Subscription ID: {subscription_id}")
    logger.debug(f"cli_ctx: {cli_ctx}")
    return get_mgmt_service_client(cli_ctx, ContainerRegistryManagementClient, subscription_id=subscription_id).registries
