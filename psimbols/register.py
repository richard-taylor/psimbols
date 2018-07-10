
import json
import logging
import os

import psimbols.client
import psimbols.config
import psimbols.err

class Register:

    def __init__(self):
        if psimbols.config.dir is not None:
            self.read_clients(psimbols.config.dir)

    def read_clients(self, dir):
        self.clients = {}
        for file in os.listdir(dir):
            filename = os.path.join(dir, file)
            try:
                with open(filename, 'r') as f:
                    config = json.load(f)
                    errors = 0
                    for property in ('client', 'server', 'key'):
                        if property not in config:
                            logging.error("No '" + property + "' in " + filename)
                            errors += 1
                            
                    if errors == 0:
                        self.clients[config['client']] = \
                            psimbols.client.Client(config['client'],
                                                   config['server'],
                                                   config['key'])
                        logging.info('Added client ' + config['client'])
                        
            except IOError:
                logging.error('Could not read file ' + filename)
            except json.JSONDecodeError:
                logging.error('Could not parse JSON file ' + filename)
                
    def get_client(self, id):
        try:
            return self.clients[id]
        except KeyError:
            return None
