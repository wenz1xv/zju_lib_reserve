import configparser

cf = configparser.ConfigParser()
cf.read('./user_data.cfg')
cf.set("user_set", "cookies", '11111')