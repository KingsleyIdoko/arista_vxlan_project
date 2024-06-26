import sys
import json
from os.path import abspath, dirname
import xmltodict
from xml.dom.minidom import parseString

# Add the project root directory to the PYTHONPATH
sys.path.insert(0, abspath(dirname(__file__) + '/..'))

from utilities_scripts.main_func import main
from nornir import InitNornir
from nornir.core.task import Task, Result
from ncclient import manager

class NetconfManager:
    def __init__(self, config_file: str):
        self.nr = InitNornir(config_file=config_file)
        self.filter = '''
            <vlan xmlns="http://openconfig.net/yang/vlan">
                <vlan>
                    <!-- VLAN specific configuration here -->
                </vlan>
            </vlan>
        '''

    def netconf_get_config(self, task: Task) -> Result:
        host = task.host.hostname
        username = task.host.username
        password = task.host.password

        try:
            with manager.connect(
                host=host,
                port=830,
                username=username,
                password=password,
                hostkey_verify=False
            ) as m:
                netconf_reply = m.get_config(source='running', filter=('subtree', self.filter))
                # netconf_reply = m.get_config(source='running')
                if self.output_format == "json":
                    netconf_dict = xmltodict.parse(netconf_reply.xml)
                    result_data = netconf_dict
                else:
                    # Pretty print the XML
                    xml_pretty = parseString(netconf_reply.xml).toprettyxml()
                    result_data = xml_pretty
                
                return Result(
                    host=task.host,
                    result=result_data
                )
        except Exception as e:
            return Result(
                host=task.host,
                result=f"Failed to connect: {str(e)}",
                failed=True
            )

    def set_output_format(self, format_choice: str):
        if format_choice not in ["json", "xml"]:
            raise ValueError("Invalid format choice. Please select 'json' or 'xml'.")
        self.output_format = format_choice

if __name__ == "__main__":
    main(NetconfManager)
