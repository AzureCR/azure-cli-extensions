.. :changelog:

Release History
===============
1.0.2
++++++
* **BREAKING**: Migrated sync command to dedicated sync API endpoint
  * Updated `az acr cache sync` command to use new cacheRuleSyncParameter endpoint instead of importImage
  * Changed from Long Running Operation (LRO) pattern to fire-and-forget queuing model
  * Added messaging to inform users that sync requests are queued and will complete asynchronously

* **FEATURE**: Added `--sync-tag-if-deleted` parameter for enhanced sync control
  * New optional flag for `az acr cache sync` command to control behavior with deleted tags
  * When enabled, allows syncing tags that have been deleted from the source registry
  * sync_tag_if_deleted parameter defaults to false when omitted

* **ENHANCEMENT**: Improved parameter handling and validation
  * Removed unused imports (ImportSource, ImportImageParameters) from legacy implementation

1.0.1
++++++
* **ENHANCEMENT**: Added deprecation warnings for legacy tag filtering parameters
  * `--starts-with`, `--ends-with`, `--contains`, `--tag` are now deprecated
  * Users should migrate to `--tag-starts-with`, `--tag-ends-with`, `--tag-contains`, `--tag-equals` respectively
  * Legacy parameters still work but display deprecation warnings with migration guidance
* **CHANGED**: Changed preview status for feature differentiation
  * Basic cache rule operations (Pull-Through Cache) are Generally Available (GA)
  * Artifact Sync functionality and related parameters remain in Preview
* **DOCUMENTATION**: Updated README and help files to guide users on new parameter usage and deprecation
* **TESTING**: Updated unittests to cover deprecation warnings and new parameter handling

1.0.0c9
++++++  
* **FEATURE**: added new artifact sync filtering options for cache rules
  * `--tag`: filter tag by exact name
* **ENHANCEMENT**:Improved error messages for invalid parameter combinations  

1.0.0c8
++++++
* **BUGFIX**: Resolved issue with sync-referrers enabled without `--sync activesync`
  * Added validation to ensure `--sync-referrers` can only be used with `--sync activesync`
  * Ensured proper validation and assignment of managed identities in `az acr cache create` and `az acr cache update` commands
  * Improved README documentation for clarity on parameter dependencies and usage examples


1.0.0c7
++++++
* **FEATURE**: Added `--assign-identity` parameter support for cache rules
  * `az acr cache create --assign-identity` - Create cache rules with user-assigned managed identities
  * `az acr cache update --assign-identity` - Update existing cache rules with managed identities
  * Enables secure authentication for ACR-to-ACR caching across subscriptions within the same tenant
  * Supports Azure resource ID format validation for managed identity resources
* **ENHANCEMENT**: Improved error handling and validation for identity parameters
* **TESTING**: Added comprehensive unit test coverage for identity processing functionality

1.0.0c6
++++++
* **BREAKING**: Migrated to Container Registry SDK v2025-09-01-preview
  * Updated SDK imports from v2025_07_01_preview to v2025_09_01_preview
  * Updated SDK client factory to support new API version
* **ENHANCEMENT**: Standardized enum values for sync and referrer status
  * Sync parameter now uses ActiveSync/PassiveSync values
  * Referrer status now uses Enabled/Disabled values
  * Added case-insensitive comparisons and improved None handling
* **REFACTOR**: Improved validation and state logic
  * Refactored input validation logic in cache.py for sync/referrer options
  * Modified CLI argument definitions in _params.py to reflect new enum values
  * Enhanced error handling and parameter validation
* **DOCUMENTATION**: Updated help examples for clarity
  * Rewrote help examples in _help.py for alignment with new conventions
  * Improved CLI documentation and usage examples
* **TESTING**: Expanded test coverage
  * Added comprehensive unit tests for cache operations and validation logic
  * Updated test coverage to support the new API version
  * Enhanced reliability testing under new SDK
* **COMPATIBILITY**: No breaking changes to CLI interface, only behavioral improvements

1.0.0
++++++
* Initial release.
