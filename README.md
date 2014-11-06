# xmlparse #

xmlparse is a library for python.

It can dump any basic python variable to a xml file, and parse it from this file.

## example ##
##### import #####
    >>> import xmlparse
    >>> from lxml import etree # just for dump
##### Simple Variables #####
    >>> a = 100
    >>> ET = xmlparse.var2xml(a)
    >>> etree.tostring(ET)
    '<xmlparse type="int">100</xmlparse>'
    >>> b = xmlparse.xml2var(ET)
    >>> print b, type(b)
    100 <type 'int'>
    >>>
    >>> a = 'test'
    >>> ET = xmlparse.var2xml(a)
    >>> etree.tostring(ET)
    '<xmlparse type="str">test</xmlparse>'
    >>> b = xmlparse.xml2var(ET)
    >>> print b, type(b)
    test <type 'str'>
##### Complex Variables #####
    >>> a = {False:'1', 10:2, 'test':'to'}
    >>> ET = xmlparse.var2xml(a)
    >>> etree.tostring(ET)
    '<xmlparse type="dict"><k0 keytype="bool" type="str">1</k0><ktest keytype="str" type="str">to</ktest><k10 keytype="int" type="int">2</k10></xmlparse>'
    >>> b = xmlparse.xml2var(ET)
    >>> print b, type(b)
    {False: '1', 'test': 'to', 10: 2} <type 'dict'>
##### Dump to File #####
    >>> a = {False:'1', 10:2, 'test':'to'}
    >>> xmlparse.var2file(a, 'test.xml')
    True
    >>> b = xmlparse.file2var('test.xml')
    >>> print b
    {False: '1', 'test': 'to', 10: 2}

