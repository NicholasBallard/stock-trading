import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement
from pprint import pprint

account = '12345'
symbol = "T"
quantity = "2"

body = \
f"""<?xml version="1.0" encoding="UTF-8"?><FIXML xmlns="http://www.fixprotocol.org/FIXML-5-0-SP2"><Order TmInForce="0" Typ="1" Side="1" Acct="{account}"><Instrmt SecTyp="CS" Sym="{symbol}"/><OrdQty Qty="{quantity}"/></Order></FIXML>"""

root = Element("root")

SubElement(root, "one")
SubElement(root, "two", first="cat", second="dog")
SubElement(root, "three")

for node in root:
    print(node)

pprint(ET.tostring(root))