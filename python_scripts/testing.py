import requests
import json

# Device details
device_ip = '192.168.1.100'
username = 'admin'
password = 'admin123'
url = f"https://{device_ip}/command-api"

# Disable warnings for insecure connections
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Command to retrieve the running config in XML format
commands = ["show running-config"]
data ={
  "jsonrpc": "2.0",
  "method": "runCmds",
  "params": {
    "format": "json",
    "timestamps": False,
    "autoComplete": True,
    "expandAliases": False,
    "includeErrorDetail": False,
    "cmds": [
      {
        "cmd": "enable",
        "input": "my_enable_passw0rd"
      },
      "show running-config"
    ],
    "version": 1
  },
  "id": "EapiExplorer-1"
}

response = requests.post(url, auth=(username, password), json=data, verify=False)
print(json.dumps(response.json(), indent=4))