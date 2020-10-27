### Prerequisites

1. [VSCode](https://code.visualstudio.com/)
2. [REST Client Extension](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)
3. `python >= 3.8` (required for saving access-token environment variable)
4. `az` cli (required for fetching the access token)

### Usage

1. Make sure to login to azure and set your subscription using `az`. Subscription `70aad6c5-69f0-4905-87b8-f8700e08e2dd` is being used for creating the resources.

```sh
az login
az account set --subscription 70aad6c5-69f0-4905-87b8-f8700e08e2dd
```

2. Run [`setBearerToken.py`](./setBearerToken.py) to patch the `Authorization` environment variable for REST Client.
3. The sample payloads are available in the [`payload`](./payload) folder. Set the contents accordingly. Please note that the json files contain variables denoted as `{variable}` which would be set accordingly when importing the payload, as the API requests are made.from [`scvmm.http`](./scvmm.http).
4. Fire the API requests in [`scvmm.http`](./scvmm.http) sequentially.
