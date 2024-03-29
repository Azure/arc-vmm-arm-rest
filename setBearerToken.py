import json
import subprocess
import os
import typing
from os.path import dirname, abspath

# %%
subscriptionId = '204898ee-cd13-4332-b9d4-55ca5c25496d'


def createJSONFile(pathToFile: str):
    json.dump({}, open(pathToFile, 'w+'), indent=2)


def setValueOfNestedKey(
    obj: typing.Dict[str, typing.Any],
    nestedKeyPath: typing.List[str],
    value,
    force=True,
):
    curr = obj
    for key in nestedKeyPath[:-1]:
        if key not in curr.keys():
            curr[key] = {}
        curr: typing.Dict[str, typing.Any] = curr[key]
    if force or nestedKeyPath[-1] not in curr:
        curr[nestedKeyPath[-1]] = value


def setBearerToken(projectRoot: str):
    cmd = f'az account get-access-token --subscription {subscriptionId}'
    out = subprocess.getoutput(cmd)
    try:
        tokenJSON = json.loads(out)
    except json.decoder.JSONDecodeError:
        print('Unable to fetch access token')
        print(out)
        return
    dotVSCodePath = f'{projectRoot}/.vscode'
    if not os.path.exists(dotVSCodePath):
        os.makedirs(dotVSCodePath)
    settingsJSONPath = f'{dotVSCodePath}/settings.json'
    if not os.path.exists(settingsJSONPath):
        createJSONFile(settingsJSONPath)
    try:
        json.load(open(settingsJSONPath, 'r'))
    except json.decoder.JSONDecodeError:
        createJSONFile(settingsJSONPath)
    finally:
        settingsJSON: typing.Dict[str, typing.Any] = json.load(
            open(settingsJSONPath, 'r')
        )

    keyPath = ['rest-client.defaultHeaders', 'Authorization']
    setValueOfNestedKey(settingsJSON, keyPath, f"Bearer {tokenJSON['accessToken']}")

    keyPath = ['rest-client.environmentVariables', '$shared', 'uni']
    setValueOfNestedKey(settingsJSON, keyPath, "xmas", force=False)

    keyPath = ['rest-client.environmentVariables', '$shared', 'armRoot']
    setValueOfNestedKey(
        settingsJSON, keyPath, "https://management.azure.com", force=False
    )
    json.dump(settingsJSON, open(settingsJSONPath, 'w'), indent=2)


setBearerToken(dirname(abspath(__file__)))
