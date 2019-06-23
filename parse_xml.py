import pandas as pd
from math import sqrt

import xml.etree.ElementTree as ET
tree = ET.parse('country_data.xml')
#enclosures = tree.findall('enclosure')
enclosures = tree.findall(".//enclosure")

for enclosure in  enclosures:
    print(enclosure.attrib)
    url = enclosure.attrib['url'].split('?')[0]
    print(url)