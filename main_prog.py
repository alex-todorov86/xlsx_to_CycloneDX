#!/usr/bin/python3
from sys import argv
import argparse
import pandas as pd
import argparse
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
parser = argparse.ArgumentParser(description='Gathers script parameters from cmdline')
parser.add_argument('--infile', '-i', metavar="input xlsx filepath", type=str,
            help='Path to the xlsx file from which the data will be read')
parser.add_argument('--outfile', '-o', metavar='output JSON filepath', type=str, default='out_file.json'
            help='Output file path')
parser.add_argument('--columns', '-c', metavar='cnames', type=str, default='Name, Type, Version, Publisher'
            help='Column names in the xlsx file from which to take data')
args = parser.parse_args()

print(args.infile)

#if __name__ == '__main__':
#    params = args_to_kwargs(argv)
#    fields = params['-fields'].split(',')
#    new_bom = CycloneDX_BOM(params['-outfile'])
#    xlsx_data = pd.read_excel(params['-infile'], sheet_name='Sheet1')
#    for i in range(0, len(xlsx_data)):
#        ctype = xlsx_data['Type'][i]
#        publisher = xlsx_data['Publisher'][i]
#        name = xlsx_data['Name'][i]
#        version = xlsx_data['Version'][i]
#        new_bom.add_component(publisher, name, version, ctype)
#    new_bom.write_out()



