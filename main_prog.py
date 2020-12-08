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

    TO-DO:
    - create variables from kwargs
    - raise exception if mandatory args are not found
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

    def __init__(self, out_file='test.json'):
        self.body = {
                   "bomFormat": "CycloneDX",
                   "specVersion": 1.2,
                   "serialNumber": "urn:uuid:{0}".format(uuid.uuid4()),
                   "version": 1,
                   "metadata": "This is a test BOM",
                   "components": [

                       ]
                    }
        self.out_file = out_file

    def add_component(self, publisher, name,
                      version, ctype):

        component = {"type": ctype, "publisher": publisher,
                     "name": name, "version": version}

        self.body['components'].append(component)

    def write_out(self):
        data = json.dumps(self.body)
        with open(self.out_file, 'w') as output:
            output.write(data)

##################################
#          MAIN CODE             #
##################################

if __name__ == '__main__':
    params = args_to_kwargs(argv)
    fields = params['-fields'].split(',')
    new_bom = CycloneDX_BOM(params['-outfile'])
    xlsx_data = pd.read_excel(params['-infile'], sheet_name='Sheet1')
    for i in range(0, len(xlsx_data)):
        ctype = xlsx_data['Type'][i]
        publisher = xlsx_data['Publisher'][i]
        name = xlsx_data['Name'][i]
        version = xlsx_data['Version'][i]
        new_bom.add_component(publisher, name, version, ctype)
    new_bom.write_out()



