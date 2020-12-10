#!/usr/bin/python3
from sys import argv
from datetime import datetime
from xml.etree.ElementTree import Element, SubElement, Comment, tostring
from xml.dom import minidom
import argparse
import pandas as pd
import argparse
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


    def _create_Body(self, file_format: str, metadata: str):
        '''
         Check what file format the output file should be and
         create a file body which to be used
         '''

        if self.isXML:
            body = Element('bom')
            body.attrib['version'] = "1"
            body.attrib['serialNumber'] = "urn:uuid:{0}".format(uuid.uuid4())
            body.attrib['xmlns'] = "http://cyclonedx.org/schema/bom/1.1"
            components = SubElement(body, 'components')

        else:
            body = {
                   "bomFormat": "CycloneDX",
                   "specVersion": 1.2,
                   "serialNumber": "urn:uuid:{0}".format(uuid.uuid4()),
                   "version": 1,
                   "metadata": metadata,
                   "components": [

                       ]
                    }

        return body

    def _xml_prettify(self, elem):
        '''
        Return a pretty-printed XML string for the Element
        '''
        rough_string = tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)

        return reparsed.toprettyxml(indent="  ")




    def __init__(self, out_file='test.xml', meta='This is a test BOM', out_format='xml'):
        if out_format.lower() == 'xml':
            self.isXML = True
        self.body = self._create_Body(out_format, meta)
        self.out_file = out_file
        self.components = ''


    def add_component(self, publisher, name,
                      version, ctype):
        '''
        Add a component to the self.body
        '''
        # cpe format:
        # cpe:2.3:<part>:<vendor>:<product>:<version>:<update>:<edition>:<language>:<sw_edition>:<target_sw>:<target_hw>:<other>
        # part entries allowed: a - for Application, h - for Hadrware, o - OS
        cpe = 'cpe:2.3:a'
        cpe += ':' + publisher
        cpe += ':' + name
        cpe += ':' + str(version)

        if self.isXML:
            component = SubElement(self.body[0], 'component')
            component.attrib['type'] = str(ctype)
            e_publisher = SubElement(component, 'publisher')
            e_publisher.text = str(publisher)
            e_name = SubElement(component, 'name')
            e_name.text = str(name)
            e_version = SubElement(component, 'version')
            e_version.text = str(version)
            e_cpe = SubElement(component, 'cpe')
            e_cpe.text = str(cpe)

        else:
            component = {"type": ctype, "publisher": publisher,
                    "name": name, "version": version, "cpe": cpe}
            self.body['components'].append(component)

    # Write the object body to a file
    def write_out(self):
        if self.isXML:
            print('Creating sBOM {0} in XML format \n'.format(self.out_file))
            with open(self.out_file, 'w') as output:
                output.write(self._xml_prettify(self.body))
        else:
            print('Creating sBOM {0} in JSON format \n'.format(self.out_file))
            with open(self.out_file, 'w') as output:
                json.dump(self.body, output, indent=1)

##################################
#          MAIN CODE             #
##################################


# Gathering and parsing of CLI arguments
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

# To be used for mapping XLSX columns to CycloneDX_BOM Component types; not yet
# ready

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

    xlsx_data = pd.read_excel(args.infile, sheet_name='Sheet1')

    # Adding data from the parsed XLSX file to the CycloneDX_BOM object

    for i in range(0, len(xlsx_data)):
        ctype = xlsx_data['Type'][i]
        publisher = xlsx_data['Publisher'][i]
        name = xlsx_data['Name'][i]
        version = xlsx_data['Version'][i]
        new_bom.add_component(publisher, name, version, ctype)

    # Writing the CycloneDX_BOM object info to file
    new_bom.write_out()


