# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
#
# Code generated by aaz-dev-tools
# --------------------------------------------------------------------------------------------

# pylint: disable=line-too-long
# pylint: disable=too-many-lines

from knack.help_files import helps  # pylint: disable=unused-import

helps['apic api register'] = """
    type: command
    short-summary: Registers a new API with version, definition, and associated deployments using the specification file as the source of truth. For now we only support OpenAPI JSON/YAML format.
    parameters:
      - name: --api-location -l
        type: string
        short-summary: Location of spec file.
      - name: --resource-group -g
        type: string
        short-summary: Resource group name.
      - name: --service-name -n
        type: string
        short-summary: APICenter Catalog or Service name.
      - name: --environment-id
        type: string
        short-summary: Id of environment created before.
    examples:
      - name: Register api by providing spec file.
        text: |
          az apic api register -g api-center-test -n contosoeuap --api-location "examples/cli-examples/spec-examples/openai.json" --environment-id public
          az apic api register -g api-center-test -n contosoeuap --api-location "examples/cli-examples/spec-examples/openai.yml" --environment-id public
      - name: Register api by providing spec url.
        text: |
          az apic api register -g api-center-test -n contosoeuap --api-location "https://petstore.swagger.io/v2/swagger.json" --environment-id public
          az apic api register -g api-center-test -n contosoeuap --api-location "https://petstore.swagger.io/v2/swagger.yaml" --environment-id public
"""
