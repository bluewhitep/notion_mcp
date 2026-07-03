# Raw API Tools

- `raw_api_invoke`
  - Description: calls a Notion SDK/API operation allowed by the Core registry.
  - Required parameters: `operation`.
  - Optional parameters: `arguments`.
  - Security: only operations registered in `src/nilo/core/services/raw_api.py` are allowed. Arbitrary attribute traversal is rejected.
- `raw_api_registered_operations`
  - Description: lists callable raw API operations.
  - Required parameters: none.
