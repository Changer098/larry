from Hosts import Hosts

class Provider:
    building = None     # e.g. YONG
    TR = None           # e.g. 286
    stack = None        # e.g. 1
    switch = None       # e.g. 3
    port = None         # e.g 18
    switchType = None   # e.g. c3750ep
    intType = None      # Gi, Te, Tw, Fa
    uplink = False      # e.g. Te1/1/3
    fex = False         # e.g. Gi101/1/0/11

    def __init__(self, risqueString=None, switchString=None):
        if risqueString is not None:
            self.__parseProviderFromRisque(risqueString)
        if switchString is not None:
            self.__parseProviderFromSwitch(switchString)

    # Fills out the provider object from a risque type
    # hamp-gu01a-c3750ep-01:04-Gi4/0/18 resolves to building: hamp, TR: gu01a, stack: 1, switch: 4
    # gcmb-100-c3560cg-01-Gi0/6 resolves to building: gcmb, TR: 100, stack: 1, switch: 0
    def __parseProviderFromRisque(self, risque):
        if risque is None:
            raise AttributeError("risqueString attribute is None")
        if type(risque) is not str:
            raise ValueError("risqueString attribute is not a string")
        if len(risque) is 0:
            raise AttributeError("risqueString is not a valid provider!")
        # ['hamp-gu01a-c3750ep-01', '04-Gi4/0/18']
        risqueSplit = risque.split(':')
        if len(risqueSplit) != 2:
            if ':' not in risque:
                # gcmb-100-c3560cg-01-Gi0/6
                # ['gcmb', '100', 'c3560cg', '01', 'Gi0/6']
                hypenSplit = risque.split('-')
                try:
                    if len(hypenSplit) is 1:
                        raise AttributeError("risqueString is not a valid provider!")
                    else:
                        self.building = hypenSplit[0]
                        self.TR = hypenSplit[1]
                        self.switchType = hypenSplit[2]
                        self.stack = int(hypenSplit[3])
                        # ['Gi0', '6']
                        interfaceSplit = hypenSplit[len(hypenSplit) - 1].split('/')
                        self.intType = interfaceSplit[0][0:len(interfaceSplit[0]) - 1]
                        self.switch = int(interfaceSplit[0][len(interfaceSplit[0]) - 1])
                        self.port = int(interfaceSplit[len(interfaceSplit)-1])
                        if len(interfaceSplit) is 3:
                            # ['Gi4', '0', '18']
                            if interfaceSplit[1] == '1':
                                self.uplink = True
                            elif int(interfaceSplit[1]) > 1:
                                raise AttributeError("risqueString is a line card, not supported!")

                except AttributeError:
                    raise
                except:
                    raise AttributeError("risqueString is not a valid provider!")
            else:
                raise AttributeError("risqueString is not a valid provider!")
            return
        # ['hamp', 'gu01a', 'c3750ep', '01']
        buildingSplit = risqueSplit[0].split('-')
        self.building = buildingSplit[0].lower()
        self.TR = buildingSplit[1].lower()
        self.stack = int(buildingSplit[3])
        self.switchType = buildingSplit[2]
        # ['04', 'Gi4/0/18']
        switchSplit = risqueSplit[1].split('-')
        self.switch = int(switchSplit[0])
        # ['Gi4', '0', '18']
        providerSplit = switchSplit[len(switchSplit) - 1].split('/')
        self.port = int(providerSplit[len(providerSplit) - 1])
        self.intType = providerSplit[0][0:len(providerSplit[0]) - 1]
        if int(providerSplit[1]) != 0:
            self.uplink = True
            if int(providerSplit[1]) != 1:
                raise AttributeError("risqueString is a line card, not supported!")

    # Fills out the provider object from the switch type
    # GigabitEthernet1/0/9 resolves to switch 1, port 9, intType: Gi
    # Gi3/0/12 resolves to switch 3, port 12, intType: Gi
    # Te1/1/3 resolves to switch 1, port 3, intType Te, uplink = True
    # Te2/3/16 doesn't resolve as it refers to a chassis
    # FastEthernet0/1 resolves to switch 0, port 1, intType Fa
    def __parseProviderFromSwitch(self, switch):
        if switch is None:
            raise AttributeError("switchString attribute is None")
        if type(switch) is not str:
            raise ValueError("switchString attribute is not a string")
        if len(switch) is 0:
            raise AttributeError("switchString is an invalid provider")
        # ['GigabitEthernet1', '0', '9'], ['Fa0', '8']
        providerSplit = switch.split('/')
        if len(providerSplit) == 4:
            # ['gi104', '1', '0', '6']
            self.fex = True
            self.port = int(providerSplit[len(providerSplit) - 1])
            self.intType = providerSplit[0][0:2]            # Assuming IntTypes can only be 2 characters
            self.switch = int(providerSplit[0][2:])
            return
        if len(providerSplit) < 2:
            raise AttributeError("switchString is an invalid provider")
        # ['Gi3', '0']
        rawType = providerSplit[0][0:len(providerSplit[0])-1]
        self.switch = int(providerSplit[0][len(providerSplit[0]) - 1])
        if len(rawType) > 2:
            if "GigabitEthernet" == rawType:
                self.intType = "Gi"
            elif "TwoGigabitEthernet" == rawType:
                self.intType = "Tw"
            elif "TenGigabitEthernet" == rawType:
                self.intType = "Te"
            elif "FastEthernet" == rawType:
                self.intType = 'Fa'
            else:
                raise AttributeError("switchSting is not a valid provider!")
        else:
            self.intType = rawType
        # ['Fa0', '8']
        if len(providerSplit) == 2:
            self.port = int(providerSplit[1])
        else:
            self.port = int(providerSplit[2])
            if providerSplit[1] != '0':
                if providerSplit[1] != '1':
                    raise AttributeError("switchString is a line card, not supported!")
                self.uplink = True

    def __str__(self):
        if self.building is not None and self.TR is not None:
            string = self.building + '-' + self.TR + '-' + self.switchType + '-' + str(self.stack)\
                   + '-' + self.intType + str(self.switch) + '/'
            if self.uplink:
                string = string + '1/'
            else:
                string = string + '0/'
            string = string + str(self.port)
            return string
        else:
            return self.getSwitchInterface()

    # Returns a host address from a given provider
    @staticmethod
    def getHostFromProvider(provider):
        if provider is None:
            return None
        if provider.building is None or provider.TR is None or provider.switchType is None:
            raise AttributeError("getHostFromProvider requires a valid building, room, and switchType")
        buildingList = Hosts.getBuildings(provider.building)
        if provider.building not in buildingList:
            raise ValueError("Invalid Building, unable to get host")
        #  search by room and switch
        filtered = Hosts.filter(buildingList, str(provider.TR), switches=True)
        for host in filtered[provider.building]:
            if Hosts.isEqual(host, provider.building, provider.TR, provider.switchType, provider.stack):
                return host
        return None

    @staticmethod
    # Assumes the TR has all the same types of UPSs (if more than one)
    # Returns the first type found
    def getUPSTypeFromProvider(provider):
        if provider is None:
            return None
        if provider.building is None or provider.TR is None:
            raise AttributeError("getUPSTypeFromProvider requires a valid building and room")
        buildingList = Hosts.getBuildings(provider.building)
        if provider.building not in buildingList:
            raise ValueError("Invalid Building, unable to get host")
        #  search by room and switch
        filtered = Hosts.filter(buildingList, str(provider.TR), ups=True)
        if filtered[provider.building] is None:
            return None
        # convert host (stew-115b-apc5000rm-01.tcom.purdue.edu) to device (apc5000rm)
        return Hosts.hostToUPSDevice(filtered[provider.building][0])

    # Returns an interface corresponding to this provider
    # e.g., gi3/0/1, te1/1/3, fa0/1, tw3/0/1
    def getSwitchInterface(self):
        if self.switch == 0:
            # e.g. fa0/1
            return "{0}0/{1}".format(self.intType, self.port)
        else:
            return "{0}{1}/{2}/{3}".format(self.intType, self.switch, (0, 1)[self.uplink], self.port)

    def isValidUPSName(self, name):
        # of type yong-664-trp1500-01
        # check building name is same, check tr is same
        # check ups model is a valid model
        # ['yong', '664', 'trp1500', '01']
        nameSplit = name.split('-')
        if nameSplit is None or len(nameSplit) < 3:
            return False
        if nameSplit[0] != self.building:
            return False
        if nameSplit[1] != self.TR:
            return False
        if nameSplit[2] not in Hosts.getUPSList():
            return False
        return True
