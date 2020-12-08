from sys import argv
import pandas as pd
from datetime import datetime
import json
import uuid


'''
Valid script arguments:
    -infile: str
    -outfile: str
    -fields: comma separated list
'''

##################################
#        FUNCTIONS BLOCK         #
##################################


def args_to_kwargs(args_list):
    '''
    Converts args to kwargs.
    An arg is considered a kwarg
    when it's preceeded with a dash (-)
    '''
    out = {}
    for i in range(1, len(args_list)):
        if args_list[i].startswith('-'):
            out[args_list[i]] = args_list[i+1]
    return out


##################################
#           CLASSES              #
##################################

class CycloneDX_BOM:

    def __init__(self, sernum)
        self.body = {
                '$schema': 'http://json-schema.org/draft-07/schema#',
                '$id': 'http://cyclonedx.org/schema/bom-1.2.schema.json',
                'type': 'object',
                'required': [
                    'bomFormat',
                    'specVersion',
                    'version'
                    ],
                'properties': {
                    'bomFormat': 'CycloneDX',
                    'specVersion': 1.2
                    'serialNumber': 'urn:uuid:{0}'.format(uuid.uuid4())
                        }

                    }
                }

    def add_component(self, publisher, name,
                      version, ctype):
        pass








##################################
#          MAIN CODE             #
##################################
kwargs = args_to_kwargs(argv)

