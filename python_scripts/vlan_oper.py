from nornir import InitNornir
from nornir_scrapli.tasks import netconf_get_config
from nornir_utils.plugins.functions import print_result

def get_config(task):
    # Perform the get-config RPC to fetch the running configuration
    result = task.run(task=netconf_get_config, source="running")
    
    # Store the result in the host's data dictionary for further processing if needed
    task.host["config"] = result.result

    # Print the raw XML data received from the device
    print(f"Config for {task.host}:\n{result.result}")

# Initialize Nornir with the configuration file
nr = InitNornir(config_file="../config.yml")

# Run the task to fetch the running configuration
results = nr.run(task=get_config)

# Print the overall task result using Nornir’s built-in print_result function
print_result(results)