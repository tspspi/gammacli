import socket

class GammaIonPump:
    def __init__(self, host, timeout=2, connection=None):
        self.sock = False
        self.host = host
        self.verbose = False

        if host is not None:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.sock.settimeout(timeout)
            self.sock.connect((host, 23))
        elif connection is not None:
            self.sock = connection
        else:
            raise ConnectionError("Failed to Connect to ion pump:\
                                              No host or connection provided")

        # Wait for initial prompt
        while True:
            chunk = self.sock.recv(1)
            if chunk == b'':
                self.sock.close()
                self.sock = False
                raise ConnectionError("Failed to Connect to ion pump:\
                                Failed to connect to pump at specified IP")
            if chunk.decode("utf-8") == ">":
                break

    def setVerbose(self, verboseState):
        self.verbose = verboseState

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.sock:
            if self.verbose:
                print("Closing socket connection")
            self.sock.close()
            self.sock = False

    def close(self):
        if self.sock:
            if self.verbose:
                print("Closing socket connection")
            self.sock.close()
            self.sock = False

    def sendCommand(self, command):
        if self.verbose:
            print("Sending command {}".format(command))
        if not self.sock:
            if self.verbose:
                print("Pump controller not connected")
            raise ConnectionError("Failed to Connect to ion pump:\
                                            Pump controller not connected")

        # Transmit command:
        self.sock.send(('spc '+command+"\r\n").encode())

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
            if repl.endswith('\r\r'):
                break
            repl = repl + chunk.decode("utf-8")

        repl = repl.strip('>\n ')
        if not repl.startswith("OK"):
            if self.verbose:
                print(f"Received error {repl}")
            return False

        return repl

    def identify(self):
        if self.verbose:
            print("Requesting identity of pump controller")

        res = self.sendCommand('01')
        if res is False:
            return False

        # Parse result
        return res[6:].strip()

    def getPressureWithUnits(self, pumpIndex):
        '''Reads ion pump pressure

        Returns:
            tuple (pressure, units) or
            False if there was a communication error or
            None if the pump is disabled or unavailable
        '''
        if self.verbose:
            print("Requesting pressure for pump {}".format(pumpIndex))

        repl = self.sendCommand('0B '+str(pumpIndex))

        if repl is False:
            if self.verbose:
                print("Failed to receive pressure information")
            return False

        repl = repl.split(" ")

        if len(repl) < 4:
            if self.verbose:
                print("Failed to read response from GammaQPC")
            return False

        units = repl[3].strip()
        if self.verbose:
            print(f"Gamma QPC set to {units}")

        pressure = float(repl[2])
        if pressure == 1.3e-11:
            if self.verbose:
                print("Pump disabled or unavailable")
            pressure = None

        if self.verbose:
            print(f"Received {pressure} {units}")
        return pressure, units
    
    def getPressure(self, pumpIndex, require_units='mBar'):
        '''Returns pump pressure in requred units'''
        response = self.getPressureWithUnits(pumpIndex)
        if not isinstance(response, tuple):
            return response
        pressure, units = response

        if units.lower() != require_units.lower():
            if self.verbose:
                print(f"Gamma QPC not set to {require_units}")
            return False
        return pressure

    def enable(self, pumpIndex):
        if self.verbose:
            print("Request enabling pump {}".format(pumpIndex))

        repl = self.sendCommand('37 '+str(pumpIndex))
        if self.verbose:
            if repl is False:
                print("Enabling pump failed")

        return repl is not False

    def disable(self, pumpIndex):
        if self.verbose:
            print("Request disabling pump {}".format(pumpIndex))

        repl = self.sendCommand('38 '+str(pumpIndex))
        if self.verbose:
            if repl is False:
                print("Disabling pump failed")

        return repl is not False

    def getVoltage(self, pumpIndex):
        if self.verbose:
            print("Requesting voltage for pump {}".format(pumpIndex))

        repl = self.sendCommand('0C '+str(pumpIndex))
        if repl is False:
            if self.verbose:
                print("Requesting voltage failed")
            return None

        # Parse response
        return int(repl[6:])

    def getCurrent(self, pumpIndex):
        if self.verbose:
            print("Requesting current for pump {}".format(pumpIndex))

        repl = self.sendCommand('0A '+str(pumpIndex))
        if repl is False:
            if self.verbose:
                print("Requesting current failed")
            return None

        repl = repl.split(" ")
        if (repl[3].strip()) != "AMPS":
            if self.verbose:
                print("Failed to decode QPC reply, unit was "+repl[3])
            return None
        return float(repl[2].strip())

    def getPumpSize(self, pumpIndex):
        if self.verbose:
            print("Requesting pump size for pump {}".format(pumpIndex))

        repl = self.sendCommand('11 '+str(pumpIndex))
        if repl is False:
            if self.verbose:
                print("Requesting pump size")
            return None

        repl = repl.split(" ")
        if (repl[3].strip()) != "L/S":
            if self.verbose:
                print("QPC unit for pump size not L/S but "+repl[3])
            return None
        return float(repl[2].strip())

    def getHighVoltageStatus(self, pumpIndex):
        '''Reads ion pump high voltages status

        Returns:
            - True or False if it's on or off
            - None if the pump's response was neither or the reply was empty
        '''
        if self.verbose:
            print("Requesting if high voltage is enabled for pump {}".format(pumpIndex))

        repl = self.sendCommand(f"61 {pumpIndex}")
        if repl is False:
            if self.verbose:
                print("Request if high voltage is enabled failed")
            return None

        repl = repl.strip()
        if repl.endswith("YES"):
            status = True
        elif repl.endswith("NO"):
            status = False
        else:
            return None

        if self.verbose and status is not None:
            print(f"High voltage {'is' if status else 'is not'} on")

        return status

    def getSupplyStatus(self, pumpIndex):
        if self.verbose:
            print("Requesting supply status for pump {}".format(pumpIndex))

        repl = self.sendCommand('0D '+str(pumpIndex))
        if repl is False:
            if self.verbose:
                print("Requesting pump size")
            return None

        return repl[6:].strip()
