# Unofficial Gamma ion pump ethernet control CLI utility and library

This is a mini Python 3 library and utility that exposes some of the functions
of the Gamma Vacuum QPC ion pump controller via a CLI or via a library class
via it's Ethernet port.

__Note__: This utility is in no way associated with Gamma Vacuum and is
_not_ an official product. It's just a simple tool that emerged out of my
requirements to interact with their pump controllers. There is no guarantee that
this utility will work under any circumstances, won't damage your controller
or will work after firmware upgrades, etc.

## Installation

This package can be installed by ```pip```. Depending on the environment
and operating system:

```
python -m pip install gammaionctl-tspspi
```

or simply

```
pip install gammaionctl-tspspi
```

In case one does not want to use ```pip``` one can also simply copy ```src/gammaionctl/gammaionctl.py```
and import from this file. There are no additional dependencies for the library.

### Uninstalling

Uninstalling the package is also directly possible using ```pip``` if it has
been installed that way:

```
python -m pip uninstall gammaionctl-tspspi
```

or

```
pip uninstall gammaionctl-tspspi
```

## Library API

The library exposes a single ```GammaIonPump``` class inside the ```gammactl```
package.

### Creating an instance / connecting

To connect to an ion pump controller one simply instantiates the ```GammaIonPump```
class passing the remote host address - one can either do this explicit and call
close after one's done:

```
pump = GammaIonPump("10.0.0.11")
# ...
pump.close()
```

Or one can use the ```with``` construct which is highly encouraged:

```
with GammaIonPump("10.0.0.11") as pump:
    # Do whatever you want
```

There is a ```setVerbose``` method that one can use to dump debug information
on ```stdout```. This is primarily thought for debugging purposes during
development though. To enable verbose mode one can simply execute

```
pump.setVerbose(True)
```

### Error handling

All methods either:

* Return a value
* Return ```None``` in case there is no measurement value such as pressure for a
  disabled pump - in this case the connection stays active
* ```False``` in case of I/O or network errors as well as protocol violations. In
  this case the connection is dropped and no further commands are possible until
  one reconnects by reinstantiation of the connection object.

### Identifying the controller

The ```identify``` method returns the identification string of the controller
or ```False``` in case of failure.

Example:

```
id = pump.identify()
print(id) # Prints "DIGITEL QPC" for our controller
```

### Getting estimated vacuum pressure

The pumps are able to estimate the current pressure inside the pump volume based
on their pumping current. The pump index has to be 1-4 for the quad pump controller.

The method returns either:

* the pressure in millibar as ```float```
* ```None``` in case there is no measurement value (for example because the
  pump is currently disabled)
* ```False``` in case of a protocol violation. Then the connection has been dropped.

```
# Querying pressure for pump 1
pressure = pump.getPressure(1)
```

### Getting pump voltage

For every pump one can query the pump voltage of the ion pump using ```getVoltage```.
Again the pump index has to be 1-4 for the quad pump controller.

The method returns either:

* the voltage in Volts as ```float```.
* ```None``` in case there is no measurement value. Note that for a disabled pump
  there is a standby current in the range of a few tens of volts that seems to be
  used to detect if there is an pump attached.
* ```False``` in case of a protocol violation. Then the connection has been dropped.

```
# Querying voltage for pump 1
volts = pump.getVoltage(1)
```

### Getting pump current

For every pump one can query the pump current of the ion pump using ```getCurrent```.
Again the pump index has to be 1-4 for the quad pump controller.

The method returns either:

* the current in Millivolts as ```float```.
* ```None``` in case there is no measurement value (for example for a disabled pump)
* ```False``` in case of a protocol violation. Then the connection has been dropped.

```
# Querying current for pump 1
amps = pump.getCurrent(1)
```

### Querying the pump size

Using ```getPumpSize``` one can query the pump capacity of the pump in liters
per second (```L/S```) for a pump index in the range from 1-4 for the quad pump
controller.

The method returns either:

* the pump capacity in liters per second as ```int```.
* ```None``` in case there is no configured size (in case no pump is connected
  for example)
* ```False``` in case of a protocol violation. Then the connection has been dropped.

```
# Querying pump capacity for pump 1
capacity = pump.getPumpSize(1)
```

### Querying the current supply status

In addition (for human interfacing) one can query the supply status - the string
shown on the controllers display - for every pump. This is done using ```getSupplyStatus```
again for a pump index in the range from 1-4 for the quad pump controller.

The method returns either:

* the pump status as ```string```.
* ```False``` in case of a protocol violation. Then the connection has been dropped.

```
# Querying pump status for pump 1
status = pump.getSupplyStatus(1)
```

### Starting and stopping a pump

To enable a pump that's currently disabled on can use the ```enable``` method,
to stop a running pump the ```disable``` method. These methods of course also
require the pump index. They either return ```True``` in case the operation
succeeded (note this is idempotent so disabling a disabled pump is successful)
or ```False``` in case of a protocol violation or connection error in which case
the connection has been dropped.

```
# Enabling pump 1
pump.enable(1)
# Disabling pump 1
pump.disable(1)
```
