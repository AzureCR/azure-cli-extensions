# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

import unittest
from unittest import mock
from unittest.mock import MagicMock
from azure.cli.testsdk import ScenarioTest, ResourceGroupPreparer
from azext_acrcssc.cssc import create_acrcssc, update_acrcssc, delete_acrcssc, show_acrcssc, cancel_runs, list_scan_status

class AcrcsscScenarioTest(ScenarioTest):

    @ResourceGroupPreparer()
    def test_acrcssc_workflow(self, resource_group):
        self.kwargs.update({
            'registry_name': self.create_random_name('clireg', 20),
            'workflow_type': 'scan',
            'config': 'path/to/config.json',
            'schedule': '7d'
        })

        self.cmd('acr create -n {registry_name} -g {rg} --sku Standard',
                 checks=[self.check('name', '{registry_name}'),
                         self.check('provisioningState', 'Succeeded')])

        self.cmd('acr supply-chain workflow create -r {registry_name} -t {workflow_type} --config {config} --schedule {schedule}',
                 checks=[self.check('workflowType', '{workflow_type}'),
                         self.check('provisioningState', 'Succeeded')])

        self.cmd('acr supply-chain workflow list -r {registry_name}',
                 checks=[self.check('[0].workflowType', '{workflow_type}')])

        self.cmd('acr supply-chain workflow show -r {registry_name} -t {workflow_type}',
                 checks=[self.check('workflowType', '{workflow_type}')])

        self.cmd('acr supply-chain workflow update -r {registry_name} -t {workflow_type} --schedule 14d',
                 checks=[self.check('schedule', '14d')])

        self.cmd('acr supply-chain workflow delete -r {registry_name} -t {workflow_type}',
                 checks=[self.check('provisioningState', 'Succeeded')])

        self.cmd('acr delete -n {registry_name} -g {rg} -y')
