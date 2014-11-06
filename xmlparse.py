r'''A bridge of XML and python basic variable

Program can dump any variable of basic type to a xml file, or read variable 
from xml file. It based on xml.etree.ElementTree module in standard. Beside 
basic type, it can support other type defined as follow:
  - datetime.datetime
'''

from lxml import etree
import os
import datetime

__all__ = ['var2file',
           'file2var']

_datetime_format = '%Y-%m-%dT%H:%M:%SZ'
_root_title = 'xmlparse'

def var2file(var, path):
    '''var2file(variable, path)

    Dump variable to a xml file.

    '''
    return xml2file(var2xml(var, _root_title), path)

def file2var(path):
    '''file2var(path)

    Read a xml file and create a variable base on it.

    '''
    ET = file2xml(path)
    if ET.getroot().tag != _root_title:
        return None
    return xml2var(ET)

def xml2file(ET, path):
    if ET is None:
        return False
    F = open(path, 'w')
    F.flush()
    F.close()
    ET.write(path, encoding='utf-8', method='xml')
    return True

def file2xml(path):
    if not os.path.exists(path):
        return None
    try:
        parser = etree.XMLParser(encoding='utf-8', recover=True)
        b = etree.parse(path, parser=parser)
        return etree.parse(path, parser=parser)
    except Exception, e:
        print "%s" % e
        return None

def var2xml(var, title='xmlparse'):
    if var is None:
        return None
    root = etree.Element(title)
    _fillsub(root, var)
    return etree.ElementTree(root)

def xml2var(ET):
    if ET is None:
        return None
    root = ET.getroot()
    return _parsesub(root)

def _numbertosymbol(number_str):
    return 'k%s' % number_str

def _symboltonumber(number_str):
    return number_str[1:]

# var parse mothed
def _fillsub(xmlElement, data):
    input_type = type(data)
    if input_type is int:
        xmlElement.attrib['type'] = 'int'
        xmlElement.text = str(data)
        return
    if input_type is long:
        xmlElement.attrib['type'] = 'long'
        xmlElement.text = str(data)
        return
    if input_type is float:
        xmlElement.attrib['type'] = 'float'
        xmlElement.text = str(data)
        return
    if input_type is str:
        xmlElement.attrib['type'] = 'str'
        xmlElement.text = data
        return
    if input_type is unicode:
        xmlElement.attrib['type'] = 'unicode'
        xmlElement.text = data
        return
    if input_type is bool:
        xmlElement.attrib['type'] = 'bool'
        if data:
            xmlElement.text = '1'
        else:
            xmlElement.text = '0'
        return
    if input_type is dict:
        xmlElement.attrib['type'] = 'dict'
        for key in data.iterkeys():
            if type(key) is int:
                key_ele = etree.SubElement(xmlElement, _numbertosymbol(str(key)))
                key_ele.attrib['keytype'] = 'int'
            elif type(key) is long:
                key_ele = etree.SubElement(xmlElement, _numbertosymbol(str(key)))
                key_ele.attrib['keytype'] = 'long'
            elif type(key) is float:
                key_ele = etree.SubElement(xmlElement, _numbertosymbol(str(key)))
                key_ele.attrib['keytype'] = 'float'
            elif type(key) is bool:
                if key:
                    key_ele = etree.SubElement(xmlElement, _numbertosymbol(str(1)))
                else:
                    key_ele = etree.SubElement(xmlElement, _numbertosymbol(str(0)))
                key_ele.attrib['keytype'] = 'bool'
            elif type(key) is unicode:
                key_ele = etree.SubElement(xmlElement, _numbertosymbol(str(key)))
                key_ele.attrib['keytype'] = 'unicode'
            else:
                key_ele = etree.SubElement(xmlElement, _numbertosymbol(str(key)))
                key_ele.attrib['keytype'] = 'str'
            _fillsub(key_ele, data[key])
        return
    if input_type is list:
        xmlElement.attrib['type'] = 'list'
        i = 0
        for value in data:
            value_ele = etree.SubElement(xmlElement, 'e' + str(i))
            _fillsub(value_ele, value)
            i += 1
        return
    if input_type is tuple:
        xmlElement.attrib['type'] = 'tuple'
        i = 0
        for value in data:
            value_ele = etree.SubElement(xmlElement, 'e' + str(i))
            _fillsub(value_ele, value)
            i += 1
        return
    if input_type is datetime.datetime:
        xmlElement.attrib['type'] = 'datetime.datetime'
        xmlElement.text = data.strftime(_datetime_format)
        return
    try:
        xmlElement.text = str(data)
        xmlElement.attrib['type'] = 'unknown'
    except:
        pass

# xml element parse mothed
def _parsesub(xmlElement):
    input_type = xmlElement.attrib.get('type', '')
    if input_type == 'int':
        return int(xmlElement.text)
    if input_type == 'long':
        return long(xmlElement.text)
    if input_type == 'float':
        return float(xmlElement.text)
    if input_type == 'str':
        return str(xmlElement.text)
    if input_type == 'unicode':
        return unicode(xmlElement.text)
    if input_type == 'bool':
        return bool(xmlElement.text)
    if input_type == 'dict':
        result = {}
        for child in xmlElement:
            key_str = _symboltonumber(child.tag)
            if child.attrib['keytype'] == 'int':
                key = int(key_str)
            elif child.attrib['keytype'] == 'long':
                key = long(key_str)
            elif child.attrib['keytype'] == 'float':
                key = float(key_str)
            elif child.attrib['keytype'] == 'bool':
                key = bool(int(key_str))
            elif child.attrib['keytype'] == 'unicode':
                key = unicode(key_str)
            elif child.attrib['keytype'] == 'str':
                key = str(key_str)
            else:
                key = child.tag
            result[key] = _parsesub(child)
        return result
    if input_type == 'list':
        result = []
        for child in xmlElement:
            result.append(_parsesub(child))
        return result
    if input_type == 'tuple':
        result = ()
        for child in xmlElement:
            result += (_parsesub(child),)
        return result
    if input_type == 'datetime.datetime':
        return datetime.datetime.strptime(str(xmlElement.text), _datetime_format)
    if input_type == 'unknown':
        return str(xmlElement.text)

        
