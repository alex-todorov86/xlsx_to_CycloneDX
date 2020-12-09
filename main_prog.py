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
    -columns: comma separated list
'''

##################################
#        FUNCTIONS BLOCK         #
##################################


##################################
#           CLASSES              #
##################################

class CycloneDX_BOM:

    isXML = False

    def _create_Body(file_format: str):
        pass



    def __init__(self, out_file='test.json', meta='This is a test BOM', out_format='xml'):
        self.body = {
                   "bomFormat": "CycloneDX",
                   "specVersion": 1.2,
                   "serialNumber": "urn:uuid:{0}".format(uuid.uuid4()),
                   "version": 1,
                   "metadata": meta,
                   "components": [

                       ]
                    }
        self.out_file = out_file
        if out_format.lower() == 'xml':
            self.isXML = True

    def add_component(self, publisher, name,
                      version, ctype):

        component = {"type": ctype, "publisher": publisher,
                     "name": name, "version": version}

        self.body['components'].append(component)

    def write_out(self):
        data = json.dumps(self.body)
        with open(self.out_file, 'w') as output:
            output.write(data)
            print('Created sBOM {0} \n'.format(self.out_file))

##################################
#          MAIN CODE             #
##################################
parser = argparse.ArgumentParser(
        description='Gathers script parameters from cmdline'
        )

parser.add_argument('--infile', '-i', metavar="input xlsx filepath", type=str,
            help='Path to the xlsx file from which the data will be read'
            )

parser.add_argument('--outfile', '-o', metavar='output JSON filepath',
        type=str, default='out_file.json',
        help='Output file path'
        )

parser.add_argument('--columns', '-c', metavar='cnames', type=str,
        default='Name, Type, Version, Publisher',
        help='Column names in the xlsx file from which to take data'
        )

parser.add_argument('--format', '-f',metavar='output file format', type=str,
        default='xml', help='The format of the output file (xml or json)')

args = parser.parse_args()
col_names = args.columns.split(',')

if __name__ == '__main__':
    '''
    Currently the code is adapted for a
    particular xlsx column naming.

    TO-DO:
    - mapping column names passed to the columns argument
      to component fields
    '''
    col_names = args.columns.split(',')
    new_bom = CycloneDX_BOM(args.outfile, meta='Ooga-Booga-Booga!', out_format=args.format)

    print('Reading xlsx file {0} ... \n'.format(args.infile))
    print(new_bom.isXML)
    xlsx_data = pd.read_excel(args.infile, sheet_name='Sheet1')
    for i in range(0, len(xlsx_data)):
        ctype = xlsx_data['Type'][i]
        publisher = xlsx_data['Publisher'][i]
        name = xlsx_data['Name'][i]
        version = xlsx_data['Version'][i]
        new_bom.add_component(publisher, name, version, ctype)

    new_bom.write_out()


