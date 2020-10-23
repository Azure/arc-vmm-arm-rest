
import json, subprocess, os, typing
from os.path import dirname, abspath
#%%
subscriptionId = '70aad6c5-69f0-4905-87b8-f8700e08e2dd'

def createJSONFile(pathToFile: str):
	json.dump({}, open(pathToFile, 'w+'), indent=2)

def setValueOfNestedKey(obj: typing.Dict[str, typing.Any], nestedKeyPath: typing.List[str], value):
	curr = obj
	for key in nestedKeyPath[:-1]:
		if key not in curr.keys():
			curr[key] = {}
		curr: typing.Dict[str, typing.Any] = curr[key]
	curr[nestedKeyPath[-1]] = value

def setBearerToken(projectRoot: str):
	cmd = f'az account get-access-token --subscription {subscriptionId}'
	out = subprocess.getoutput(cmd)
	tokenJSON = json.loads(out)
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
		settingsJSON: typing.Dict[str, typing.Any] = json.load(open(settingsJSONPath, 'r'))
	
	keyPath = ['rest-client.environmentVariables', 'local', 'bearerToken']
	setValueOfNestedKey(settingsJSON, keyPath, tokenJSON['accessToken'])
	json.dump(settingsJSON, open(settingsJSONPath, 'w'), indent=2)

setBearerToken(dirname(abspath(__file__)))
