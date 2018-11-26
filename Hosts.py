import os


class Hosts:
    # Get all the hosts for each building requested
    # Returns a list of the buildings requested
    @staticmethod
    def getBuildings(buildings):
        # Accept strings, lists, and sets
        if not isinstance(buildings, set) and not isinstance(buildings, list) and not isinstance(buildings, basestring):
            raise Exception("getBuildings() only accepts strings, lists, and sets")
        if not isinstance(buildings, set) and not isinstance(buildings, list):
            #  single object, make it a list
            tmp = buildings
            buildings = list()
            buildings.append(tmp)
        if Hosts.isLinux():
            hostDict = dict()  # [buildings] -> array(hostnames)

            try:
                lines = open("/etc/hosts").readlines()
            except IOError:
                print("Couldn't read HOSTS file: {0}".format(IOError))
                return None

            inZone = False
            for line in lines:
                if len(line) == 0:
                    continue
                if line[0] == '#':
                    # Find Zone: tcom.purdue.edu
                    if "Zone:" in line and "tcom.purdue.edu" in line:
                        inZone = True
                        continue
                if inZone:
                    hostname = Hosts.__splitHost(line)
                    #  print("SplitHostname: {0}".format(hostname))
                    buildingName = hostname.split('-')[0]
                    #  print("BuildingName: {0}".format(buildingName))
                    for building in buildings:
                        if building == buildingName:
                            if building not in hostDict:
                                hostDict[building] = list()
                            hostDict[building].append(hostname)
                            break
            return hostDict
        else:
            raise OSException()

    @staticmethod
    def getAllHosts():
        hostDict = None
        if Hosts.isLinux():
            hostDict = dict()  # [buildings] -> array(hostnames)

            try:
                lines = open("/etc/hosts").readlines()
            except IOError:
                print("Couldn't read HOSTS file: {0}".format(IOError))
                return None

            inZone = False
            for line in lines:
                if len(line) == 0:
                    continue
                if line[0] == '#':
                    # Find Zone: tcom.purdue.edu
                    if "Zone:" in line and "tcom.purdue.edu" in line:
                        inZone = True
                        continue
                if inZone:
                    hostname = Hosts.__splitHost(line)
                    #  print("SplitHostname: {0}".format(hostname))
                    buildingName = hostname.split('-')[0]
                    if not buildingName in hostDict:
                        hostDict[buildingName] = list()
                    hostDict[buildingName].append(hostname)
        return hostDict

    # Returns True if Linux and false for everything else
    @staticmethod
    def isLinux():
        if os.name == "posix":
            return True
        else:
            return False

    @staticmethod
    def getChassisList():
        return {
            "c4500x",
            "c4507",
            "c6504e",
            "c6506",
            "c6509",
            "c9006"
        }

    @staticmethod
    def getSwitchList():
        return {
            "c2350",
            "c2950a",
            "c2960xp",
            "c2960xpg",
            "c2960x",
            "c2960sp",
            "c3512",
            "c3550",
            "c3560cg",
            "c3560eg",
            "c3560cx",
            "c3560",
            "c3750e",
            "c3750x",
            "c3750g",
            "c3750ep",
            "c3750eb",
            "c3850",
            "c3850mg",
            "c4948",
            "c4948x",
            "c6800",
            "c9348uxm",
        }

    #  Removes all but (if true) switches and (if true) chassis
    #  if vlan, don't reject vlan hosts
    @staticmethod
    def filter(hostList, room, switches=False, chassis=False, vlan=False):
        Switches = Hosts.getSwitchList()
        Chassis = Hosts.getChassisList()
        if not isinstance(switches, bool) or not isinstance(chassis, bool) or not isinstance(vlan, bool):
            print("filter() was give non-boolean parameters")
            return None
        if not isinstance(hostList, dict):
            print("filter() was given a non-dict parameter")
            return None
        if room is not None and not isinstance(room, str):
            print("filter() was given a non-string parameter")
            return None

        newHosts = dict()
        for key in hostList:
            for value in hostList[key]:
                if value is None:
                    continue
                if "vlan" in value:
                    if not vlan:
                        continue
                if room is not None:
                    if room not in value:
                        continue
                device = Hosts.__getHostDevice(value)
                buildingName = value.split('-')[0]
                if switches:
                    if device in Switches:
                        #  print("{0} in Switches".format(value))
                        if buildingName not in newHosts:
                            newHosts[buildingName] = list()
                        newHosts[buildingName].append(value)
                if chassis:
                    if device in Chassis:
                        if buildingName not in newHosts:
                            newHosts[buildingName] = list()
                        newHosts[buildingName].append(value)
        return newHosts

    # Return hostname
    @staticmethod
    def __splitHost(hostline):
        #  123.1.4.5\tyong-601-blah becomes yong-601-blah
        split = hostline.strip().split('\t')
        return split[1]

    @staticmethod
    # Return host device
    def __getHostDevice(hostname):
        split = hostname.strip().split('-')
        if len(split) >= 4:
            return split[2]
        return None

    @staticmethod
    # Return true if a hostname contains the values
    def isEqual(hostname, building, room, device, stack):
        if hostname is None:
            return False
        if building is None or room is None or device is None or stack is None:
            raise AttributeError("isEqual must be given a building, room, device, and stack to compare against")
        # valid host: mann-b032-c3750ep-01.tcom.purdue.edu
        hostSplit = hostname.split('-')
        if len(hostSplit) != 4:
            raise AttributeError("hostname is an invalid hosttype")
        if hostSplit[0] != building:
            return False
        if hostSplit[1] != str(room):
            return False
        if hostSplit[2] != device:
            return False
        if hostSplit[3] != str(stack):
            return False
        return True


class OSException(Exception):
    def __init__(self):
        super(Exception, self).__init__("Only Linux Hosts are supported")