#!/usr/bin/env python3

from gammaionctl import gammaionctl
import time, sys

def printUsage():
    print("Gamma ion pump controller (QPC) remote control utility")
    print("This is not an official tool and not associated with Gamma vacuum")
    print("Find this tool online at: https://www.github.com/")
    print("")
    print("Usage:")
    print("\t{} [settings] <commands>".format(sys.argv[0]))
    print("")
    print("Settings:")
    print("\t--host ADDRESS\tSets the remote hostname or IP")
    print("")
    print("Commands (status, controller):")
    print("\tid\t\tIdentifies the remote QPC")
    print("")
    print("Commands (status, per pump):")
    print("\tpres N\t\tFetches pressure for pump N")
    print("\tvolt N\t\tFetches voltage (in volts) for pump N")
    print("\tcur N\t\tFetches current in milliamps for pump N")
    print("\tsize N\t\tGets size of pump N in L/S")
    print("\tstatus N\tGets current pump status (as on display)")
    print("")
    print("Commands (actions, per pump):")
    print("\ton N\t\tEnabled pump N")
    print("\toff N\t\tDisabled pump N")
    print("Commands (actions, local):")
    print("\tsleep N\tSleeps N seconds")

def gammaioncli():
    host = None

    if len(sys.argv) < 2:
        printUsage()

    # First gather all settings

    skipArg = 0;
    for i in range(1, len(sys.argv)):
        if skipArg > 0:
            skipArg = skipArg - 1
            continue
        if sys.argv[i].strip() == "--host":
            if i == (len(sys.argv)-1):
                print("Missing host specification")
                sys.exit(2)
                break
            host = sys.argv[i+1]
            skipArg = 1
        elif sys.argv[i].strip() == "id":
            pass
        elif sys.argv[i].strip() == "pres":
            if i == (len(sys.argv)-1):
                print("Missing pump index for preassure query")
                sys.exit(2)
                break
            pumpidx = 0
            try:
                pumpidx = int(sys.argv[i+1])
            except:
                print("Failed to interpret pump index "+sys.argv[i+1])
                sys.exit(2)
                break
            if (pumpidx > 4) or (pumpidx < 1):
                print("Invalid pump index "+sys.argv[i+1])
                sys.exit(2)
                break
            skipArg = 1
        elif sys.argv[i].strip() == "volt":
            if i == (len(sys.argv)-1):
                print("Missing pump index for voltage query")
                sys.exit(2)
                break
            pumpidx = 0
            try:
                pumpidx = int(sys.argv[i+1])
            except:
                print("Failed to interpret pump index "+sys.argv[i+1])
                sys.exit(2)
                break
            if (pumpidx > 4) or (pumpidx < 1):
                print("Invalid pump index "+sys.argv[i+1])
                sys.exit(2)
                break
            skipArg = 1
        elif sys.argv[i].strip() == "cur":
            if i == (len(sys.argv)-1):
                print("Missing pump index for current query")
                sys.exit(2)
                break
            pumpidx = 0
            try:
                pumpidx = int(sys.argv[i+1])
            except:
                print("Failed to interpret pump index "+sys.argv[i+1])
                sys.exit(2)
                break
            if (pumpidx > 4) or (pumpidx < 1):
                print("Invalid pump index "+sys.argv[i+1])
                sys.exit(2)
                break
            skipArg = 1
        elif sys.argv[i].strip() == "size":
            if i == (len(sys.argv)-1):
                print("Missing pump index for size query")
                sys.exit(2)
                break
            pumpidx = 0
            try:
                pumpidx = int(sys.argv[i+1])
            except:
                print("Failed to interpret pump index "+sys.argv[i+1])
                sys.exit(2)
                break
            if (pumpidx > 4) or (pumpidx < 1):
                print("Invalid pump index "+sys.argv[i+1])
                sys.exit(2)
                break
            skipArg = 1
        elif sys.argv[i].strip() == "status":
            if i == (len(sys.argv)-1):
                print("Missing pump index for status query")
                sys.exit(2)
                break
            pumpidx = 0
            try:
                pumpidx = int(sys.argv[i+1])
            except:
                print("Failed to interpret pump index "+sys.argv[i+1])
                sys.exit(2)
                break
            if (pumpidx > 4) or (pumpidx < 1):
                print("Invalid pump index "+sys.argv[i+1])
                sys.exit(2)
                break
            skipArg = 1
        elif sys.argv[i].strip() == "on":
            if i == (len(sys.argv)-1):
                print("Missing pump index for pump startup")
                sys.exit(2)
                break
            pumpidx = 0
            try:
                pumpidx = int(sys.argv[i+1])
            except:
                print("Failed to interpret pump index "+sys.argv[i+1])
                sys.exit(2)
                break
            if (pumpidx > 4) or (pumpidx < 1):
                print("Invalid pump index "+sys.argv[i+1])
                sys.exit(2)
                break
            skipArg = 1
        elif sys.argv[i].strip() == "off":
            if i == (len(sys.argv)-1):
                print("Missing pump index for pump shutdown")
                sys.exit(2)
                break
            pumpidx = 0
            try:
                pumpidx = int(sys.argv[i+1])
            except:
                print("Failed to interpret pump index "+sys.argv[i+1])
                sys.exit(2)
                break
            if (pumpidx > 4) or (pumpidx < 1):
                print("Invalid pump index "+sys.argv[i+1])
                sys.exit(2)
                break
            skipArg = 1
        elif sys.argv[i].strip() == "sleep":
            if i == (len(sys.argv)-1):
                print("Missing duration of sleep period (in seconds)")
                sys.exit(2)
                break
            duration = 0
            try:
                duration = int(sys.argv[i+1])
            except:
                print("Failed to interpret sleep duration "+sys.argv[i+1])
                sys.exit(2)
                break
            if (duration < 1):
                print("Invalid sleep duration "+sys.argv[i+1])
                sys.exit(2)
                break
            skipArg = 1
        else:
            print("Unsupported command or setting "+sys.argv[i])

    if host == None:
        print("Missing host specification.")
        print("This is required to connect to the controller")
        sys.exit(1)

    try:
        with gammaionctl.GammaIonPump(host) as pump:
                skipArg = 0;
                for i in range(1, len(sys.argv)):
                    if skipArg > 0:
                        skipArg = skipArg - 1
                        continue
                    if sys.argv[i].strip() == "--host":
                        skipArg = 1
                    if sys.argv[i].strip() == "id":
                        res = pump.identify()
                        if res:
                            print("QPC Identity: {}".format(res))
                        else:
                            print("QPC Identity: Failed to query")
                    if sys.argv[i].strip() == "pres":
                        pumpidx = int(sys.argv[i+1])
                        res = pump.getPressure(pumpidx)
                        if res:
                            print("Pressure pump {}: {:e} mbar".format(pumpidx, res))
                        else:
                            print("Pressure pump {}: Failed to query".format(pumpidx))
                        skipArg = 1
                    if sys.argv[i].strip() == "volt":
                        pumpidx = int(sys.argv[i+1])
                        res = pump.getVoltage(pumpidx)
                        if res:
                            print("Voltage pump {}: {} V".format(pumpidx, res))
                        else:
                            print("Voltage pump {}: Failed to query".format(pumpidx))
                        skipArg = 1
                    if sys.argv[i].strip() == "cur":
                        pumpidx = int(sys.argv[i+1])
                        res = pump.getCurrent(pumpidx)
                        if res:
                            print("Current pump {}: {} mA".format(pumpidx, res))
                        else:
                            print("Current pump {}: Failed to query".format(pumpidx))
                        skipArg = 1
                    if sys.argv[i].strip() == "size":
                        pumpidx = int(sys.argv[i+1])
                        res = pump.getPumpSize(pumpidx)
                        if res:
                            print("Size of pump {}: {} L/S".format(pumpidx, res))
                        else:
                            print("Size of pump {}: Failed to query".format(pumpidx))
                        skipArg = 1
                    if sys.argv[i].strip() == "status":
                        pumpidx = int(sys.argv[i+1])
                        res = pump.getSupplyStatus(pumpidx)
                        if res:
                            print("Supply status of pump {}: {}".format(pumpidx, res))
                        else:
                            print("Supply status of pump {}: Failed to query".format(pumpidx))
                        skipArg = 1
                    if sys.argv[i].strip() == "on":
                        pumpidx = int(sys.argv[i+1])
                        res = pump.enable(pumpidx)
                        if res:
                            print("Power pump {}: enabled".format(pumpidx))
                        else:
                            print("Power pump {}: failed to enable".format(pumpidx))
                        skipArg = 1
                    if sys.argv[i].strip() == "off":
                        pumpidx = int(sys.argv[i+1])
                        res = pump.disable(pumpidx)
                        if res:
                            print("Power pump {}: standby".format(pumpidx))
                        else:
                            print("Power pump {}: failed to disable".format(pumpidx))
                        skipArg = 1
                    if sys.argv[i].strip() == "sleep":
                        duration = int(sys.argv[i+1])
                        time.sleep(duration)
                        skipArg = 1
    except Exception as e:
        pass
