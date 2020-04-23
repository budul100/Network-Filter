import locale
import re

NS = 'http://graphml.graphdrawing.org/xmlns'
FileInput = '.\\files\\Network.graphml'
FileOutput = '.\\files\\Network_Filtered.graphml'
LatitudeMin = 51.20819904748029
LatitudeMax = 51.86919568633337
LongitudeMin = -1.043067303801770
LongitudeMax = 0.6900259579169798

def withNamespace(element):
    return '{'+NS+'}'+element

def getFloat(num):
    return locale.atof(num)

def outputFile(root, fout):
    output = ET.tostring(root).decode()

    #dirty fix for adding decalration and remove namespace
    xmlDeclaration = '<?xml version="1.0" encoding="utf-8"?>\n'
    output = re.sub("<ns0:", "<", output)
    output = re.sub("</ns0:", "</", output)
    output = re.sub("xmlns:ns0", "xmlns", output)
    output = xmlDeclaration + output

    #write and flush into file
    outputFile = open(fout, "w")
    outputFile.write(output)
    outputFile.close()

loc = locale.getlocale()
locale.setlocale(locale.LC_ALL, 'de_DE')

import xml.etree.ElementTree as ET
tree = ET.parse(FileInput)

root = tree.getroot()
graph = root.find(f'{withNamespace("graph")}')

for node in graph.findall(f'{withNamespace("node")}'):

    latitude = node.find(f'.//{withNamespace("data")}[@key="d4"]').text
    longitude = node.find(f'.//{withNamespace("data")}[@key="d5"]').text

    if latitude and longitude:

        removeNode = getFloat(latitude) < LatitudeMin or getFloat(latitude) > LatitudeMax \
            or getFloat(longitude) < LongitudeMin or getFloat(longitude) > LongitudeMax
        
        if removeNode:

            nodeid = node.attrib['id']

            for edge in graph.findall(f'.//{withNamespace("edge")}[@source="{nodeid}"]'):
                graph.remove(edge)

            for edge in graph.findall(f'.//{withNamespace("edge")}[@target="{nodeid}"]'):
                graph.remove(edge)

            graph.remove(node)

for node in graph.findall(f'{withNamespace("node")}'):

    nodeid = node.attrib['id']
    removeNode = (graph.find(f'.//{withNamespace("edge")}[@source="{nodeid}"]') is None) \
        and (graph.find(f'.//{withNamespace("edge")}[@target="{nodeid}"]') is None)

    if removeNode:
        graph.remove(node)

locale.setlocale(locale.LC_ALL, loc)

outputFile(root, FileOutput)