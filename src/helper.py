import configparser
from classes import Config


def loadConfig():

    subscription_key = Config.find_by_name("C7 Key")
    
    if subscription_key is None:
        try:
            # Read from config file
            config = configparser.ConfigParser()
            files_read = config.read("colleague7.cfg")
            
            # Load subscription key from config
            subscription_key = Config("C7 Key",config.get('APIKEYS', 'SUBSCRIPTION_KEY1'))
            user_id = Config("C7 Userid",config.get('APIKEYS', 'C7_USERID'))
            ch_key = Config("CH Key",config.get('APIKEYS', 'CH_KEY'))

        except Exception as e:
            print(e)
            exit(0)

    return("Config Loaded")