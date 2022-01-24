from netmiko import ConnectHandler

host = '10.165.240.214'
username = 'montanaro'
password = '123456789'

huawei = {'device_type': 'huawei', 'host': host, 'username': username, 'password': password, "fast_cli": False, }

net_connect = ConnectHandler(**huawei)

config_commands = ['info-center loghost 10.240.150.34 source-ip ' + host + ' facility local6 port 5440',
                   'info-center trapbuffer size 1024',
                   'info-center timestamp debugging format-date without-timezone',
                   'info-center timestamp log date without-timezone',
                   'info-center timestamp trap format-date without-timezone',
                   'dis cur | in info-center'
                   ]
output = net_connect.send_config_set(config_commands)
print(output)
