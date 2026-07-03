# Raw API Tools

- `raw_api_invoke`
  - 説明: Core registry で許可された Notion SDK/API operation を呼び出します。
  - Required parameters: `operation`.
  - Optional parameters: `arguments`.
  - Security: `src/nilo/core/services/raw_api.py` に登録された operation だけを許可します。
- `raw_api_registered_operations`
  - 説明: 呼び出し可能な raw API operations を一覧します。
  - Required parameters: none.
