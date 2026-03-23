import yaml
from netmiko import ConnectHandler
from pathlib import Path


def load_yaml_file(path):
    try:
        with open(path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        return {}



def main():
    try:
        hosts = load_yaml_file(Path('./inventory.yaml'))
        if len(hosts) == 0:
            print("No hosts found")
        else:
            for host in hosts:
                net_connect = ConnectHandler(**host)
                output = net_connect.send_command(['show ip int brief',
                                                  "show ip int stats",])
                print(output)
    except Exception as e:
        print(e)

main()