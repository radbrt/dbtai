import yaml
import os
import appdirs

def get_config():
    configdir = appdirs.user_data_dir("dbtai", "dbtai")

    with open(os.path.join(configdir, "config.yaml"), "r") as f:
        return yaml.load(f, Loader=yaml.FullLoader)
    
