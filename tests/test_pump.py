'''Unit tests

Run by running `python -m unittest` from this dir.
Need to have gammaionctl installed in your viratual environment
'''
import unittest
from collections import deque
from gammaionctl import GammaIonPump

class FakeConnection:
    def __init__(self):
        self.response = deque([])

    def set_response(self, response):
        self.response = deque([ bytes(el, 'ascii') for el in response ])

    def reset(self):
        self.response.clear()

    def recv(self, buf):
        return self.response.popleft()

    def send(self, message):
        pass

    def close(self):
        pass

class TestPump(unittest.TestCase):
    def setUp(self):
        self.fake_connection = FakeConnection()
        self.fake_connection.set_response('>')
        self.pump = GammaIonPump(host=None, connection=self.fake_connection)
#        self.pump.verbose = True
        self.fake_connection.reset()

    def test_send_command(self):
        self.fake_connection.set_response('ER\r\r>')
        repl = self.pump.sendCommand('')
        self.assertFalse(repl, 'sendCommand Error Response Failed')

        self.fake_connection.set_response('OK OK\r\r>')
        repl = self.pump.sendCommand('')
        self.assertTrue(repl, 'sendCommand Failed')

    def test_identify(self):
        self.fake_connection.set_response('OK 00 PUMPITY\r\r>')
        self.assertEqual(self.pump.identify(), 'PUMPITY', 'Pump Identity Failed')

    def test_get_pressure(self):
        self.fake_connection.set_response('OK 00 1.2E-10 Torr\r\r>')
        pressure = self.pump.getPressure(1, require_units='mBar')
        self.assertFalse(pressure, 'Failed to require units')

        self.fake_connection.set_response('OK 00 1.2E-10 Torr\r\r>')
        pressure = self.pump.getPressure(1, require_units='Torr')
        self.assertEqual(pressure, 1.2e-10, 'Fetch Pump Pressure Failed')

    def test_get_pressure_with_units(self):
        self.fake_connection.set_response('OK 00 1.9E-10 Torr\r\r>')
        pressure, units = self.pump.getPressureWithUnits(1)
        self.assertEqual(pressure, 1.9e-10, 'Fetch Pump Pressure Failed')
        self.assertEqual(units, 'Torr', 'Fetch Pump Pressure Failed')

    def test_get_voltage(self):
        self.fake_connection.set_response('OK 00 7000\r\r>')
        self.assertEqual(self.pump.getVoltage(1), 7000, 'Fetch Pump Voltage Failed')

    def test_get_current(self):
        self.fake_connection.set_response('OK 00 9.0E-08 AMPS\r\r>')
        self.assertAlmostEqual(self.pump.getCurrent(1), 9.0e-8, 'Fetch Pump Current Failed')

    def test_get_pump_size(self):
        self.fake_connection.set_response('OK 00 040.0 L/S\r\r>')
        self.assertEqual(self.pump.getPumpSize(1), 40, 'Pump Size Failed')

    def test_get_high_voltage_status(self):
        self.fake_connection.set_response('OK 00 YES\r\r>')
        self.assertEqual(self.pump.getHighVoltageStatus(1), True, 'High Voltage Check Failed')

        self.fake_connection.set_response('OK 00 NO\r\r>')
        self.assertEqual(self.pump.getHighVoltageStatus(1), False, 'High Voltage Check Failed')

    def test_get_supply_status(self):
        self.fake_connection.set_response('OK 00 RUNNING\r\r>')
        self.assertEqual(self.pump.getSupplyStatus(1), 'RUNNING', 'Fetch Supply Status Failed')
        self.fake_connection.set_response('OK 00 STAND\r\r>')
        self.assertEqual(self.pump.getSupplyStatus(1), 'STAND', 'Fetch Supply Status Failed')
