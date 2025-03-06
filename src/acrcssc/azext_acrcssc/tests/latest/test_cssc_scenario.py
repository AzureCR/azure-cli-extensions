# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from azure.cli.testsdk import ScenarioTest, ResourceGroupPreparer

class AcrcsscScenarioTest(ScenarioTest):

    @ResourceGroupPreparer()
    def test_acrcssc_workflow(self, resource_group):
        self.kwargs.update({
            'registry_name': self.create_random_name('clireg', 20),
            'rg': resource_group,
            'location': 'eastus',
            'workflow_type': 'ContinuousPatchV1',
            'config': 'path/to/config.json',
            'schedule': '7d'
        })

        self.cmd('acr create -n {registry_name} -g {rg} --sku Standard --location {location}',
                 checks=[self.check('name', '{registry_name}'),
                         self.check('provisioningState', 'Succeeded')])

        self.cmd('acr supply-chain workflow create -r {registry_name} -g {rg} -t {workflow_type} --config {config} --schedule {schedule}',
                 checks=[self.check('workflowType', '{workflow_type}'),
                         self.check('provisioningState', 'Succeeded')])

        self.cmd('acr supply-chain workflow list -r {registry_name} -g {rg} -t {workflow_type}',
                 checks=[self.check('[0].workflowType', '{workflow_type}')])

        self.cmd('acr supply-chain workflow show -r {registry_name} -g {rg} -t {workflow_type}',
                 checks=[self.check('workflowType', '{workflow_type}')])

        self.cmd('acr supply-chain workflow update -r {registry_name} -g {rg} -t {workflow_type} --schedule 14d',
                 checks=[self.check('schedule', '14d')])

        self.cmd('acr supply-chain workflow delete -r {registry_name} -g {rg} -t {workflow_type} --yes',
                 checks=[self.check('provisioningState', 'Succeeded')])

        self.cmd('acr delete -n {registry_name} -g {rg} -y')
