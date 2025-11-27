import os
from configparser import ConfigParser

def load_config(filename='database.ini', section='postgresql'):
    parser = ConfigParser()
    if not os.path.exists(filename):
        raise FileNotFoundError(f"{filename} not found")

    parser.read(filename)

    config = {}
    if parser.has_section(section):
        for param in parser.items(section):
            config[param[0]] = param[1]
    else:
        raise Exception(f"Section {section} not found in {filename}")

    return config

if __name__ == "__main__":
    config = load_config("/Users/adilbekpirnazarov/Desktop/pp2/10/9/database.ini")
    print(config)
