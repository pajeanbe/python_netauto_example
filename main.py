import yaml
from netmiko import ConnectHandler
with open("inventory.yaml", "r") as ymlfile:
    hosts = yaml.safe_load(ymlfile)

for host in hosts:
    net_connect = ConnectHandler(**host)
    output = net_connect.send_command('show ip int brief')
    print(f'The output for {host['host']} is : ')
    print(output)
