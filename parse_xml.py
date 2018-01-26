import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element, SubElement, dump
from pprint import pprint

account = '12345'
symbol = "T"
quantity = "2"

body = \
f"""<?xml version="1.0" encoding="UTF-8"?><FIXML xmlns="http://www.fixprotocol.org/FIXML-5-0-SP2"><Order TmInForce="0" Typ="1" Side="1" Acct="{account}"><Instrmt SecTyp="CS" Sym="{symbol}"/><OrdQty Qty="{quantity}"/></Order></FIXML>"""

params = {
    "time_in_force": "0",
    "trade_type": "1",
    "side": "1",
    "account": account,
    "security_type": "CS",
    "symbol": symbol,
    "quantity": quantity,
}

xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>'

declaration = Element(xml_declaration)
root = Element("FIXML", {'xmlns': 'http://www.fixprotocol.org/FIXML-5-0-SP2'})
order = SubElement(root, "Order", {"TmInForce": f'{params["time_in_force"]}', "Typ": f'{params["trade_type"]}', "Side": f'{params["side"]}', "Acct": f'{params["account"]}'})
SubElement(order, "Instrmt", {"SecTyp": f'{params["security_type"]}', "Sym": f'{params["symbol"]}'})
SubElement(order, "OrdQty", {"Qty": f'{params["quantity"]}'})

pprint(ET.tostring(root, encoding='utf8', method='xml'))