from netmiko import ConnectHandler

device = {
    'device_type': 'huawei',
    'host': '10.165.240.214',
    'username': 'montanaro',
    'password': 'Am15171924',
    'global_delay_factor': 0.1,
}

netmiko_connect = ConnectHandler(**device)

netmiko_connect.find_prompt()

print("Connecting to Device:")

config_commands = ["dis cur | in info"]

output = netmiko_connect.send_config_set(config_commands, delay_factor=0.2)

netmiko_connect.disconnect()

print(output)
