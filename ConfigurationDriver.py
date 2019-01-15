from BufferedSsh import BufferedSsh
from shitSsh import shitSsh
from Ssh import Ssh
from PasswordUtility import PasswordUtility


class ConfigurationDriver:
    user = None
    switchPassword = None
    risquePassword = None
    cookies = None

    @staticmethod
    def getDriver():
        return Ssh(ConfigurationDriver.user, ConfigurationDriver.switchPassword)

    @staticmethod
    def getCredentials():
        if not ConfigurationDriver.credentialsStored():
            userName = raw_input("Risque Username: ")
            risquepassword = PasswordUtility.getpassword("Risque Password (BoilerKey): ")
            switchpassword = PasswordUtility.getpassword("Switch Password: ")
            ConfigurationDriver.storeCredentials(userName, risquepassword, switchpassword)
        return ConfigurationDriver.user, ConfigurationDriver.risquePassword, ConfigurationDriver.switchPassword

    @staticmethod
    def storeCredentials(username, risquePassword, switchPassword):
        ConfigurationDriver.user = username
        ConfigurationDriver.switchPassword = switchPassword
        ConfigurationDriver.risquePassword = risquePassword

    @staticmethod
    def credentialsStored():
        return ConfigurationDriver.user is not None

    @staticmethod
    def storeCookies(cookies):
        try:
            keys = cookies.keys()
            ConfigurationDriver.cookies = dict()
            for key in keys:
                ConfigurationDriver.cookies[key] = cookies[key]
            print "Stored cookies: {0}".format(ConfigurationDriver.cookies)
        except:
            print "failed storing cookies"
            ConfigurationDriver.cookies = None

    @staticmethod
    def cookiesStored():
        print "Cookies stored: {0}".format(ConfigurationDriver.cookies)
        return ConfigurationDriver.cookies is not None

    @staticmethod
    def getCookies():
        return ConfigurationDriver.cookies