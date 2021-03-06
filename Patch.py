from Hosts import Hosts


class Patch:
    building = None         # bown
    room = None             # 1111a
    panelNumber = None      # 02-XX
    portNumber = None       # XX-04
    patchType = None        # pp24/c6app24, c6pp24, pp48

    def __init__(self, risqueString=None):
        if risqueString is not None:
            self.__parsePatchFromRisque(risqueString)

    def __parsePatchFromRisque(self, risqueString):
        # frny-4001a-pp24-04-19 (back)
        spaceSplit = risqueString.split(' ')    # ['frny-4001a-pp24-04-19', '(back)']
        if len(spaceSplit) != 2:
            raise AttributeError("Spaces - Unrecogized patch panel format")
        dashSplit = spaceSplit[0].split('-')    # ['frny', '4001a', 'pp24', '04', '19']
        if len(dashSplit) != 5:
            raise AttributeError("Dashes - Unrecogized patch panel format")
        self.building = dashSplit[0]
        self.room = dashSplit[1]
        self.patchType = dashSplit[2]
        self.panelNumber = int(dashSplit[3])
        self.portNumber = int(dashSplit[4])

    @staticmethod
    def getHostsFromPatch(patch):
        if patch is None:
            return None
        if patch.building is None or patch.room is None:
            raise AttributeError("getHostsFromPatch requires a valid building and room")
        buildingList = Hosts.getBuildings(patch.building)
        if patch.building not in buildingList:
            raise ValueError("Invalid Building, unable to get host")
        #  search by room and switch
        filtered = Hosts.filter(buildingList, str(patch.room), switches=True)
        hosts = []
        for host in filtered[patch.building]:
            if Hosts.isEqual(host, patch.building, patch.room, None, None):
                hosts.append(host)
        if len(hosts) == 0:
            return None
        else:
            return hosts

    def __str__(self):
        return "{0}-{1}-{2}-{3}-{4}".format(self.building, self.room, self.patchType, self.panelNumber, self.portNumber)
