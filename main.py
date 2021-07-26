import paramiko
from paramiko import SSHClient, SSHConfig, SSHException
import subprocess
import time
import re
import json
import sys
import datetime
from ftplib import FTP
import uuid
import signal
import requests

iplist = []
timelist = []
login = 'montanaro'
passwd = 'Am15171924'


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
            mass = "CONFIG_BACKUP"
            ssh = paramiko.SSHClient()
            ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            filetemp = time.strftime("%Y-%m-%d -- %H:%M:%S")
            initime = time.strftime("%H:%M:%S")
            tempip = iplist[line]
            accessport = 22
            x_count = 0
            comment = "PROCESSO DE REALIZAÇÃO DE CONFIGURAÇÃO: " + filetemp + " DO HOST:  DE IP: " + iplist[line]
            print(comment)
            configname = "CONFIG__" + iplist[line] + "__" + filetemp
            ssh.connect(iplist[line], username=login, password=passwd, port=accessport, look_for_keys=False,
                        allow_agent=False)
            time.sleep(5)
            stdin, stdout, stderr = ssh.exec_command('system-view')
            time.sleep(5)
            stdin, stdout, stderr = ssh.exec_command('info-center loghost 10.240.150.34 source-ip ' + iplist[line] + ' facility local6 port 5440')
            time.sleep(5)
            stdin, stdout, stderr = ssh.exec_command('info-center trapbuffer size 1024')
            time.sleep(5)
            stdin, stdout, stderr = ssh.exec_command('info-center timestamp debugging format-date without-timezone')
            time.sleep(5)
            stdin, stdout, stderr = ssh.exec_command('info-center timestamp log date without-timezone')
            time.sleep(5)
            stdin, stdout, stderr = ssh.exec_command('info-center timestamp trap format-date without-timezone')
            time.sleep(5)

            print("Aguardando...")
            configresult = stdout.read()
            pass
            print("config FINALIZADA NO IP ", iplist[line], " às ", datatime)


        except Exception as e: #Essa exceção irá tratar caso o script não consiga logar na porta 22
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

        except paramiko.ssh_exception.AuthenticationException as mikoerr2:
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

        finally:
            ssh.close()
            signal.alarm(0)


config_mass()
