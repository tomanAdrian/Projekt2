import time
import re

from paramiko import Channel
from abc import abstractmethod
from paramiko.client import SSHClient, AutoAddPolicy
from src.core.config import settings, TypeOfConnection
from src.api.validators.Validators import TypeOfValidation, validateOutputFromConsole
from src.api.validators.Validators import CommandExecutionError
from paramiko import AuthenticationException
from paramiko.ssh_exception import NoValidConnectionsError
from fastapi import status
from py_libs.telnetlib_updated import Telnet

def detect_manufacturer_from_prompt(prompt: str) -> str:
    prompt = prompt.strip().lower()

    # MikroTik prompt vyzerá ako [admin@mikrotik] > alebo [admin@R1] >
    if re.search(r'\[.*@.*\]\s*>', prompt):
        return "mikrotik"

    # Cisco prompt vyzerá ako hostname# alebo hostname>
    if prompt.endswith('#') or prompt.endswith('>'):
        return "cisco"

    # Defaultne Cisco (radšej to zmeniť na výstrahu alebo neznámy typ)
    return "cisco"


class Communication:
    def __init__(self):
        self.connection = SSHClient()
        self.connection.set_missing_host_key_policy(AutoAddPolicy())
        self.tConnection: Telnet = Telnet()

    def initConnection(self, host: str, username: str, password: str, port: int, typeOfConnection: TypeOfConnection):
        if typeOfConnection == TypeOfConnection.SSH:
            try:
                self.connection.connect(hostname=host, username=username, password=password, port=port,
                                        look_for_keys=False,
                                        allow_agent=False)
            except AuthenticationException as e:
                raise CommandExecutionError(status_code=status.HTTP_401_UNAUTHORIZED,
                                            message="{" + f'"detail": "Unable to initiate SSH connection. Check your credentials", "host": "{host}", "port": "{port}", "user": "{username}"' + "}")
            except Exception as e:
                raise CommandExecutionError(status_code=status.HTTP_401_UNAUTHORIZED,
                                            message="{" + f'"detail": "Unable to initiate SSH connection.", "host": "{host}", "port": "{port}", "user": "{username}"' + "}")

        else:
            try:
                self.tConnection = Telnet(host=host, port=port, timeout=5.0)
            except Exception as e:
                raise CommandExecutionError(status_code=status.HTTP_401_UNAUTHORIZED, message="{" + f'"detail": "Unable to initiate Telnet conncetion", "host": "{host}", "port": "{port}"' + "}")
            self.getRoot(user=username, password=password)

    def closeConnection(self):
        self.connection.close()

    @abstractmethod
    def invokeShell(self) -> Channel:
        pass

    @abstractmethod
    def executeCommand(self, command: dict[str, any], shell: Channel = None, sleepTime: float = settings.SLEEP_TIME):
        pass

    @abstractmethod
    def getRoot(self, user: str = None, password: str = None):
        pass


class SshShellCommunication(Communication):

    def getRoot(self, user: str = None, password: str = None):
        return

    def invokeShell(self) -> Channel:
        return self.connection.invoke_shell()

    def executeCommand(self, command: dict[str, any], shell=None, sleepTime=settings.SLEEP_TIME):
        clearBuffer(shell=shell)
        shell.send(command['command'])
        time.sleep(sleepTime)
        output = clearBuffer(shell=shell)
        if output is not None:
            output = output.decode('ascii')
        else:
            output = ''
        if command['validation'] != TypeOfValidation.NONE:
            validateOutputFromConsole(output=output, typeOfValidation=command['validation'])
        return output


class SshExecCommunication(Communication):

    def getRoot(self, user: str = None, password: str = None):
        pass

    def invokeShell(self) -> Channel:
        return None

    def executeCommand(self, command: dict[str, any], shell=None, sleepTime=settings.SLEEP_TIME):
        stdin, stdout, stderr = self.connection.exec_command(command=command['command'])
        output = stdout.read().decode('ascii')
        if command['validation'] != TypeOfValidation.NONE:
            validateOutputFromConsole(output=output, typeOfValidation=command['validation'])
        return output


class TelnetCommunication(Communication):

    def enterCommand(self, command: str, validation: TypeOfValidation) -> str:
        sOutput: str = ''
        c: str = command.replace('\n', '\r\n') if command.find('\n') != -1 else command + '\r\n'
        cByte: bytes = c.encode('ascii')
        self.tConnection.write(cByte)

        # if validation != TypeOfValidation.NONE:
        bOutput: bytes = self.tConnection.read_all()
        sOutput = bOutput.decode('ascii')
        sOutput = strip_ansi_codes(sOutput)
        index = sOutput.rfind(c)
        sOutput = sOutput[sOutput.rfind(c):]
        return sOutput
    
    
    
    def getRoot(self, user: str = None, password: str = None):
        root: str
        bFirstLine: bytes = self.tConnection.read_all()
        sFirstLine: str = bFirstLine.decode('ascii')
        sFirstLine = sFirstLine[len(sFirstLine) - 20:]
        self.manufacturer = detect_manufacturer_from_prompt(sFirstLine)
        if sFirstLine.find('#') == - 1 and sFirstLine.find('>') == - 1:
            self.tConnection.write('\r\n'.encode('ascii'))
            bFirstLine: bytes = self.tConnection.read_all()
            sFirstLine: str = bFirstLine.decode('ascii')
            sFirstLine = sFirstLine[len(sFirstLine) - 40:]
            if sFirstLine.find('Login') != -1 or sFirstLine.find('Username') != -1:
                self.tConnection.write((user + '\r\n').encode('ascii'))
                time.sleep(1)
                self.tConnection.write((password + '\r\n').encode('ascii'))
                time.sleep(1.5)
                bFirstLine: bytes = self.tConnection.read_all()
                bFirstLine = bFirstLine[len(bFirstLine) - 50:]
                sFirstLine: str = bFirstLine.decode('ascii')
                sFirstLine = sFirstLine[len(sFirstLine) - 20:]
                if sFirstLine.find('Login') != -1:
                    raise CommandExecutionError(status_code=status.HTTP_401_UNAUTHORIZED,
                                                message="{" + f'"detail": "Incorrect login credentials", "user": "{user}"' + "}")
            elif sFirstLine.find('#') != - 1 or sFirstLine.find('>') != - 1:
                pass
            else:
                raise CommandExecutionError(status_code=status.HTTP_401_UNAUTHORIZED,
                                            message="{" + f'"detail": "Something went wrong during login", "advice": "Please consider using SSH instead of Telnet", "user": "{user}"' + "}")
        if sFirstLine.find('#') != -1 or sFirstLine.lower().find('cisco') != -1:
            root = '#'
            while sFirstLine.find(')#') != -1:
                sFirstLine = self.enterCommand('exit', TypeOfValidation.NONE)
        else:
            root = '>'
            self.tConnection.write('/\r\n'.encode('ascii'))

    def invokeShell(self) -> Channel:
        return None

    def executeCommand(self, command: dict[str, any], shell=None, sleepTime=settings.SLEEP_TIME):
        c: str = command['command']
        if command['validation'] == TypeOfValidation.ENABLE:
            self.tConnection.write('\r\n'.encode('ascii'))
            bOutput: bytes = self.tConnection.read_all()
            sOutput: str = bOutput.decode('ascii')
            if sOutput[len(sOutput) - 20:].find('#') == - 1:
                self.tConnection.write(c.replace('\n', '\r\n').encode('ascii'))
                bFirstLine: bytes = self.tConnection.read_all()
                sFirstLine: str = bFirstLine.decode('ascii')
                sOutput = sFirstLine[len(sFirstLine) - 20:]
        else:
            sOutput = self.enterCommand(command=c, validation=command['validation'])
        if command['validation'] != TypeOfValidation.NONE:
            validateOutputFromConsole(output=sOutput, typeOfValidation=command['validation'])
        return sOutput

    def closeConnection(self):
        self.tConnection.close()


def clearBuffer(shell: Channel):
    if shell.recv_ready():
        return shell.recv(settings.MAX_BUFFER)


"""
method for mikrotik -> used for removal of ANSI codes (colorful output)
https://github.com/jbronikowski/ftd-connector/blob/master/ftd_connector.py
"""
def strip_ansi_codes(s):
    """
    >>> import blessings
    >>> term = blessings.Terminal()
    >>> foo = 'hidden'+term.clear_bol+'foo'+term.color(5)+'bar'+term.color(255)+'baz'
    >>> repr(strip_ansi_codes(foo))
    u'hiddenfoobarbaz'
    """
    return re.sub(r'\x1b\[([0-9,A-Z]{1,2}(;[0-9]{1,2})?(;[0-9]{3})?)?[m|K]?', '', s)
