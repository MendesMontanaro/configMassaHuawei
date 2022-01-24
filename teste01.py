import time
import signal
import netmiko
import logging

logging.basicConfig(filename='logs.log', level=logging.DEBUG)
logger = logging.getLogger('netmiko')

iplist = []
timelist = []
login = 'montanaro'
passwd = '123456789'


class TimeoutException(Exception):
    pass


def timeout_handler(signum, frame):
    raise TimeoutException


signal.signal(signal.SIGALRM, timeout_handler)


def colect_list():
    # COLETA DE LISTAS DE HOSTNAMES (CIDADES), DEVICES (DISPOSITIVOS), IPS(IPS PUBLICOS DOS CONCENTRADORES")
    with open("data/ips.txt", "r") as ip_temp:
        for row03 in ip_temp:
            iplist.append(row03.replace("\n", ""))


colect_list()
# print(len(iplist))

iplength = len(iplist)
datatime = time.strftime("%Y-%m-%d")


def config_mass():
    for line in range(0, iplength):
        signal.alarm(60)

        try:
            mass = "CONFIG_HUAWEI"

            filetemp = time.strftime("%Y-%m-%d -- %H:%M:%S")
            initime = time.strftime("%H:%M:%S")
            tempip = iplist[line]
            host = {"host": iplist[line], "username": "montanaro", "password": "123456789", "device_type": "huawei",
                    "global_delay_factor": 0.1, "conn_timeout": 15, }
            x_count = 0
            comment = "PROCESSO DE REALIZAÇÃO DE CONFIGURAÇÃO: " + filetemp + " DO HOST:  DE IP: " + iplist[line]
            print(comment)
            configname = "CONFIG__" + iplist[line] + "__" + filetemp

            net_connect = netmiko.Netmiko(**host)
            command1 = ["dis cur | in info"]  # Enter set of commands
            print("Connected to:", net_connect.find_prompt())  # Display hostname
            output = net_connect.send_config_set(command1, delay_factor=.5)  # Run set of commands in order

            # Increase the sleeps for just send_command by a factor of 2
            net_connect.disconnect()  # Disconnect from Session
            print(output)

            pass
            print("config FINALIZADA NO IP ", iplist[line], " às ", datatime)


        except Exception as e:  # Essa exceção irá tratar caso o script não consiga logar na porta 22
            arqconfig = open("erroconfig" + datatime + ".txt", "a+")
            arqconfig.write("Erro no login através da porta 22 no ip - " + tempip + ":" + str(e) + "\n")
            arqconfig.close()
            signal.alarm(0)
            # print(e)
            continue

        except ValueError as e2:
            arqconfig = open("erroconfig" + datatime + ".txt", "a+")
            arqconfig.write("Erro na coinfig de ip: " + tempip + ": " + str(e2) + "\n")
            arqconfig.close()
            signal.alarm(0)
            continue

        except netmiko.ssh_exception.AuthenticationException as mikoerr2:
            arqconfig = open("erroconfig" + datatime + ".txt", "a+")
            arqconfig.write("Erro na config de ip: " + tempip + ": " + str(mikoerr2) + "\n")
            arqconfig.close()
            signal.alarm(0)
            continue

        except TimeoutException:
            arqconfig = open("erroconfig" + datatime + ".txt", "a+")
            arqconfig.write("Erro na config de ip: " + tempip + ":Tempo de execução expirado.\n")
            arqconfig.close()
            signal.alarm(0)
            continue

        except KeyboardInterrupt:
            print("\n Parando ")

        finally:
            signal.alarm(0)


config_mass()
