import unittest
from unittest.mock import Mock, patch, call
from azure.core.serialization import NULL as AzureCoreNull
from acrcache.azext_acrcache import cache

# Patch imports from the module under test
with patch("acrcache.azext_acrcache.cache.get_registry_by_name") as mock_get_registry_by_name, \
    patch("acrcache.azext_acrcache.cache.user_confirmation") as mock_user_confirmation, \
    patch("acrcache.azext_acrcache.cache.CacheRule") as MockCacheRule, \
    patch("acrcache.azext_acrcache.cache.ArtifactSyncScopeFilterProperties") as MockArtifactSyncScopeFilterProperties, \
    patch("acrcache.azext_acrcache.cache._create_kql") as mock_create_kql:


    class TestAcrCacheCreate(unittest.TestCase):
       def setUp(self):
          self.cmd = Mock()
          self.cmd.cli_ctx = Mock()
          self.client = Mock()
          self.registry = Mock()
          self.registry.id = "/subscriptions/xxx/resourceGroups/rg/providers/Microsoft.ContainerRegistry/registries/myreg"
          self.rg = "rg"
          mock_get_registry_by_name.return_value = (self.registry, self.rg)
          self.mock_cache_rule = Mock()
          MockCacheRule.return_value = self.mock_cache_rule
          self.mock_scope_filter = Mock()
          MockArtifactSyncScopeFilterProperties.return_value = self.mock_scope_filter
          mock_create_kql.side_effect = lambda s, e, c: "KQL_QUERY"

         # Test for basic cache rule creation
       def test_basic_create(self):
          self.client.begin_create.return_value = "result"
          result = cache.acr_cache_create(
             self.cmd, self.client, "myreg", "rule1", "repo1", "targetrepo"
          )
          self.assertEqual(result, "result")
          self.client.begin_create.assert_called_once()
          self.assertEqual(self.mock_cache_rule.name, "rule1")
          self.assertEqual(self.mock_cache_rule.source_repository, "repo1")
          self.assertEqual(self.mock_cache_rule.target_repository, "targetrepo")
          self.assertEqual(self.mock_cache_rule.credential_set_resource_id, AzureCoreNull)
          self.assertEqual(self.mock_cache_rule.artifact_sync_status, "Inactive")
          self.assertEqual(self.mock_cache_rule.artifact_sync_scope_filter_properties, self.mock_scope_filter)

         # Test for cache rule creation with credential set
       def test_with_cred_set(self):
          cache.acr_cache_create(
             self.cmd, self.client, "myreg", "rule1", "repo1", "targetrepo", cred_set="mycred"
          )
          self.assertEqual(
             self.mock_cache_rule.credential_set_resource_id,
             f"{self.registry.id}/credentialSets/mycred"
          )

         # Test for cache rule creation with dry run 
       def test_with_tag_in_source_repo(self):
          result = cache.acr_cache_create(
             self.cmd, self.client, "myreg", "rule1", "repo1:mytag", "targetrepo"
          )
          self.assertEqual(self.mock_cache_rule.source_repository, "repo1")
          self.assertEqual(self.mock_cache_rule.name, "rule1")
          self.assertIn("mytag", self.mock_cache_rule.artifact_sync_scope_filter_properties.query)

         # Test for cache rule creation with artifact sync enabled
       def test_with_sync_and_dry_run(self):
          cache.acr_cache_create(
             self.cmd, self.client, "myreg", "rule1", "repo1", "targetrepo", sync=True, dry_run=True
          )
          mock_user_confirmation.assert_not_called()

         # Test for cache rule creation with artifact sync enabled and no dry run
       def test_with_sync_and_no_dry_run(self):
          cache.acr_cache_create(
             self.cmd, self.client, "myreg", "rule1", "repo1", "targetrepo", sync=True, dry_run=False
          )
          mock_user_confirmation.assert_called_once()

         # Test for cache rule creation with startswith, endswith, contains
       def test_with_startswith_endswith_contains(self):
          cache.acr_cache_create(
             self.cmd, self.client, "myreg", "rule1", "repo1", "targetrepo",
             starts_with="abc", ends_with="xyz", contains="foo"
          )
          mock_create_kql.assert_called_with("abc", "xyz", "foo")
          self.assertEqual(self.mock_cache_rule.artifact_sync_scope_filter_properties.query, "KQL_QUERY")

         # Test for platforms
         # This feature is not implemented yet, so we expect an exception
       def test_with_platforms(self):
            
           with self.assertRaises(Exception) as cm:
               cache.acr_cache_create(
                   self.cmd, self.client, "myreg", "rule1", "repo1", "targetrepo",
                   platforms=["linux"]
               )
           self.assertIn("not implemented", str(cm.exception))
           # Test for sync referrers
         # This feature is not implemented yet, so we expect an exception
       def test_with_sync_referrers(self):
           with self.assertRaises(Exception) as cm:
               cache.acr_cache_create(
                   self.cmd, self.client, "myreg", "rule1", "repo1", "targetrepo",
                   sync_referrers=True
               )
           self.assertIn("not implemented", str(cm.exception))
           
         # Test for include artifact types
         # This feature is not implemented yet, so we expect an exception
       def test_with_include_artifact_types(self):
           with self.assertRaises(Exception) as cm:
               cache.acr_cache_create(
                   self.cmd, self.client, "myreg", "rule1", "repo1", "targetrepo",
                   include_artifact_types=["foo"]
               )
           self.assertIn("not implemented", str(cm.exception))

         # Test for exclude artifact types
         # This feature is not implemented yet, so we expect an exception
       def test_with_exclude_artifact_types(self):
           with self.assertRaises(Exception) as cm:
               cache.acr_cache_create(
                   self.cmd, self.client, "myreg", "rule1", "repo1", "targetrepo",
                   exclude_artifact_types=["bar"]
               )
           self.assertIn("not implemented", str(cm.exception))

         # Test for both include and exclude artifact types
       def test_include_and_exclude_artifact_types(self):
          with self.assertRaises(Exception) as cm:
             cache.acr_cache_create(
                self.cmd, self.client, "myreg", "rule1", "repo1", "targetrepo",
                include_artifact_types=["foo"], exclude_artifact_types=["bar"]
             )
          self.assertIn("cannot specify both", str(cm.exception))

    class TestAcrCacheUpdate(unittest.TestCase): 
      def setUp(self):
         self.cmd = Mock()
         self.cmd.cli_ctx = Mock()
         self.client = Mock()
         self.registry = Mock()
         self.registry.id = "/subscriptions/xxx/resourceGroups/rg/providers/Microsoft.ContainerRegistry/registries/myreg"
         self.rg = "rg"
         mock_get_registry_by_name.return_value = (self.registry, self.rg)
         self.mock_cache_rule = Mock()
         MockCacheRule.return_value = self.mock_cache_rule
         self.mock_scope_filter = Mock()
         MockArtifactSyncScopeFilterProperties.return_value = self.mock_scope_filter
         mock_create_kql.side_effect = lambda s, e, c: "KQL_QUERY"

      # Test for basic cacherule update
      def test_update_cred_set(self):
         self.client.begin_update.return_value = "result"
         result = cache.acr_cache_update(
             self.cmd, self.client, "myreg", "rule1", cred_set="newcred"
         )
         self.assertEqual(result, "result")
         self.client.begin_update.assert_called_once()
         self.assertEqual(self.mock_cache_rule.credential_set_resource_id, f"{self.registry.id}/credentialSets/newcred")
         self.assertEqual(self.mock_cache_rule.name, "rule1")
         self.assertEqual(self.mock_cache_rule.artifact_sync_status, "Inactive")

      # Test for removing cred set
      def test_remove_cred_set(self):
         self.client.begin_update.return_value = "result"
         result = cache.acr_cache_update(
             self.cmd, self.client, "myreg", "rule1", remove_cred_set=True
         )
         self.assertEqual(result, "result")
         self.client.begin_update.assert_called_once()
         self.assertEqual(self.mock_cache_rule.credential_set_resource_id, AzureCoreNull)
         self.assertEqual(self.mock_cache_rule.name, "rule1")
         self.assertEqual(self.mock_cache_rule.artifact_sync_status, "Inactive")

      # Test for sync without any filters
      def test_update_with_sync(self):
         self.client.begin_update.return_value = "result"
         result = cache.acr_cache_update(
             self.cmd, self.client, "myreg", "rule1", sync=True, starts_with="v1", ends_with="beta"
         )
         self.assertEqual(result, "result")
         self.client.begin_update.assert_called_once()
         self.assertEqual(self.mock_cache_rule.artifact_sync_status, "Active")
         self.assertEqual(self.mock_cache_rule.artifact_sync_scope_filter_properties.query, "KQL_QUERY")

      # Test for sync with dry_run
      def test_update_with_sync_and_dry_run(self): 
         self.client.begin_update.return_value = "result"
         result = cache.acr_cache_update(
             self.cmd, self.client, "myreg", "rule1", sync=True, dry_run=True
         )
         self.assertEqual(result, "result")
         self.client.begin_update.assert_called_once()
         self.assertEqual(self.mock_cache_rule.artifact_sync_status, "Active")
         self.assertEqual(self.mock_cache_rule.artifact_sync_scope_filter_properties.query, "KQL_QUERY") 
         mock_user_confirmation.assert_not_called()

      # Test for sync with dry_run
      def test_update_with_sync_and_no_dry_run(self):
         self.client.begin_update.return_value = "result"
         result = cache.acr_cache_update(
             self.cmd, self.client, "myreg", "rule1", sync=True, dry_run=False
         )
         self.assertEqual(result, "result")
         self.client.begin_update.assert_called_once()
         self.assertEqual(self.mock_cache_rule.artifact_sync_status, "Active")
         self.assertEqual(self.mock_cache_rule.artifact_sync_scope_filter_properties.query, "KQL_QUERY")
         mock_user_confirmation.assert_called_once()

      # Test for startswith, endswith, contains
      def test_update_with_startswith_endswith_contains(self):
         self.client.begin_update.return_value = "result"
         result = cache.acr_cache_update(
             self.cmd, self.client, "myreg", "rule1",
             starts_with="abc", ends_with="xyz", contains="foo"
         )
         self.assertEqual(result, "result")
         mock_create_kql.assert_called_with("abc", "xyz", "foo")
         self.assertEqual(self.mock_cache_rule.artifact_sync_scope_filter_properties.query, "KQL_QUERY")

      # Test for platforms
      def test_update_with_platforms(self):
         with self.assertRaises(Exception) as cm:
            cache.acr_cache_update(
                self.cmd, self.client, "myreg", "rule1", platforms=["linux"]
            )
         self.assertIn("not implemented", str(cm.exception))

      # Test for sync referrers
      def test_update_with_sync_referrers(self):   
         with self.assertRaises(Exception) as cm:
            cache.acr_cache_update(
                self.cmd, self.client, "myreg", "rule1", sync_referrers=True
            )
         self.assertIn("not implemented", str(cm.exception))

      # Test for include artifact types
      def test_update_with_include_artifact_types(self):
         with self.assertRaises(Exception) as cm:
            cache.acr_cache_update(
                self.cmd, self.client, "myreg", "rule1", include_artifact_types=["foo"]
            )
         self.assertIn("not implemented", str(cm.exception))

      # Test for exclude artifact types
      def test_update_with_exclude_artifact_types(self):
         with self.assertRaises(Exception) as cm:
            cache.acr_cache_update(
                self.cmd, self.client, "myreg", "rule1", exclude_artifact_types=["bar"]
            )
         self.assertIn("not implemented", str(cm.exception))

      # Test for both include and exclude artifact types
      def test_update_include_and_exclude_artifact_types(self):
         with self.assertRaises(Exception) as cm:
            cache.acr_cache_update(
                self.cmd, self.client, "myreg", "rule1",
                include_artifact_types=["foo"], exclude_artifact_types=["bar"]
            )
         self.assertIn("cannot specify both", str(cm.exception))
         mock_user_confirmation.assert_not_called()

if __name__ == "__main__":
    unittest.main()
