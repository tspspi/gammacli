import socket

class GammaIonPump:
    def __init__(self, host):
        self.sock = False
        self.host = host

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(2)
        self.sock.connect((host, 23))

        self.verbose = False

        # Wait for initial prompt
        while True:
            chunk = self.sock.recv(1)
            if chunk == b'':
                self.sock.close()
                self.sock = False
                raise
            if chunk.decode("utf-8") == ">":
                break


    def setVerbose(self, verboseState):
        self.verbose = verboseState

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.sock != False:
            if self.verbose:
                print("Closing socket connection")
            self.sock.close()
            self.sock = False

    def close(self):
        if self.sock != False:
            if self.verbose:
                print("Closing socket connection")
            self.sock.close()
            self.sock = False

    def sendCommand(self, command):
        if self.verbose:
            print("Sending command {}".format(command))
        if self.sock == False:
            if self.verbose:
                print("Pump controller not connected")
            raise

        # Transmit command:
        self.sock.send((command+"\r\n").encode())

        # Wait for reply and read till next prompt
        repl = ''
        while True:
            chunk = self.sock.recv(1)
            if chunk == b'':
                if self.verbose:
                    print('Failed to receive')
                self.sock.close()
                self.sock = False
                return False
            if chunk.decode("utf-8") == ">":
                break
            repl = repl + chunk.decode("utf-8")

        if repl[0:2] != "OK":
            if self.verbose:
                print("Received error {}".format(repl))
            return False

        return repl

    def identify(self):
        if self.verbose:
            print("Requesting identity of pump controller")

        res = self.sendCommand('spc 01')
        if res == False:
            return False

        # Parse result
        return res[6:].strip()

    def getPressure(self, pumpIndex):
        if self.verbose:
            print("Requesting pressure for pump {}".format(pumpIndex))

        repl = self.sendCommand('spc 0B '+str(pumpIndex))

        if repl == False:
            if self.verbose:
                print("Failed to receive pressure information")
            return False

        repl = repl.split(" ")

        if(len(repl) < 4):
            if self.verbose:
                print("Failed to read response from GammaQPC")
            return False

        if(repl[0] != "OK"):
            if self.verbose:
                print("Failed to read response from GammaQPC")
            return False

        if(repl[3] != 'MBAR\r\r\n'):
            if self.verbose:
                print("Gamma QPC not set to MBAR")
            return False

        pressure = float(repl[2])
        if pressure == 1.3e-11:
            if self.verbose:
                print("Pump disabled or unavailable")
            return None
        else:
            if self.verbose:
                print("Received {} mbar".format(pressure))
            return pressure

    def enable(self, pumpIndex):
        if self.verbose:
            print("Request enabling pump {}".format(pumpIndex))

        repl = self.sendCommand('spc 37 '+str(pumpIndex))
        if self.verbose:
            if repl == False:
                print("Enabling pump failed")

        return repl != False

    def disable(self, pumpIndex):
        if self.verbose:
            print("Request disabling pump {}".format(pumpIndex))

        repl = self.sendCommand('spc 38 '+str(pumpIndex))
        if self.verbose:
            if repl == False:
                print("Disabling pump failed")

        return repl != False

    def getVoltage(self, pumpIndex):
        if self.verbose:
            print("Requesting voltage for pump {}".format(pumpIndex))

        repl = self.sendCommand('spc 0C '+str(pumpIndex))
        if repl == False:
            if self.verbose:
                print("Requesting voltage failed")
            return None

        # Parse response
        return int(repl[6:])

    def getCurrent(self, pumpIndex):
        if self.verbose:
            print("Requesting current for pump {}".format(pumpIndex))

        repl = self.sendCommand('spc 0A '+str(pumpIndex))
        if repl == False:
            if self.verbose:
                print("Requesting current failed")
            return None

        repl = repl.split(" ")
        if (repl[3].strip()) != "AMPS":
            if self.verbose:
                print("Failed to decode QPC reply, unit was "+repl[3])
            return None
        return float(repl[2].strip())*1000.0

    def getPumpSize(self, pumpIndex):
        if self.verbose:
            print("Requesting pump size for pump {}".format(pumpIndex))

        repl = self.sendCommand('spc 11 '+str(pumpIndex))
        if repl == False:
            if self.verbose:
                print("Requesting pump size")
            return None

        repl = repl.split(" ")
        if (repl[3].strip()) != "L/S":
            if self.verbose:
                print("QPC unit for pump size not L/S but "+repl[3])
            return None
        return float(repl[2].strip())

    def getSupplyStatus(self, pumpIndex):
        if self.verbose:
            print("Requesting supply status for pump {}".format(pumpIndex))

        repl = self.sendCommand('spc 0D '+str(pumpIndex))
        if repl == False:
            if self.verbose:
                print("Requesting pump size")
            return None

        return repl[6:-2].strip()
