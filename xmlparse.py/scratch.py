import lxml
import requests
import urllib
import sys
import bs4
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import selenium
import pathlib
from pathlib import Path

# Common Definitions

commonDefinitions = {

   'record':  'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/e17683ce-cb4c-4968-bd7a-ebfe5cc18a1e',
   'multiByteInt31': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/1dddf488-1aaa-48c7-bfde-5cb30982ec3c',
   'multiByteInt31-1byte': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/c63c7a72-c4f1-4323-bc45-9b9b4ec0d9a3',
   'multiByteInt31-2bytes': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/9dad2a5a-8466-4a6e-8411-af8c2023f983',
   'multiByteInt31-3bytes': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/020e7d8d-158d-45ea-a7a8-d63683e39c14',
   'multiByteInt31-4Bytes': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/2379c71d-db79-4f89-97cf-78086c2675ec',
   'multiByteInt31-5Bytes': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/93e8dab1-8ccd-4b18-bcd9-b0e6a8f59ded',
   'string': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/cc9e00dc-ecc5-4a61-8869-3bd6c3f9c71a',
   'dictionaryString': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/a2cfe597-3927-4704-b456-ad435a549b1c'
   
}

elementLinks = {
   'shortElementRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/70fd89e4-04cc-4266-bfe0-9b39ce86e134',
   'elementRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/8d0c4de1-d007-4487-a1a2-8ec14cb0f15a',
   'shortDictionaryElementRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/1141f786-ebaa-4763-9cca-e903c89cd54e',
   'dictionaryElementRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/0742dbcb-dccd-47db-a1d9-8a0f67fa5be6',
   'prefixDictionaryElementRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/7d7e7d81-3640-413c-be88-4ff92c499bd0',
   'prefixElementRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/36359e79-9545-4379-9fcf-d00147605ec2'
}

elementHex = {
   'shortElementRecord': '0x40',
   'elementRecord': '0x41',
   'shortDictionaryElementRecord': '0x42',
   'dictionaryElementRecord': '0x43',
   'prefixDictionaryElement[A-Z]Record': '0x44-0x5D',
   'prefixElement[A-Z]Record': '0x5E-0x77',
}

attributeLinks = {
   'shortAttributeRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/6714ac21-d905-49c1-af0b-6c987e9a7080',
   'attributeRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/651c4957-413c-4864-b308-a8ef18c13798',
   'shortDictionaryAttributeRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/0c380954-bc47-4503-b46f-184d05702de3',
   'dictionaryAttributeRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/fcd84188-568a-4436-87a2-3548f0d8282e',
   'shortXmlnsAttributeRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/c1999b4e-d35e-4e36-80bb-a1d2dccf2935',
   'xmlnsAttributeRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/8a1d81b3-1cff-4422-9e4c-bbee16fc603e',
   'shortDictionaryXmlnsAttributeRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/aaf4dcc4-984e-4e81-aa4d-cb4a16ce992c',
   'dictionaryXmlsAttributeRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/992dd1d1-d8e4-43c8-9ac6-44860984ce53',
   'prefixDictionaryAttributeRecords': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/9c58c7e9-31fc-4959-972b-b34fa146ae36',
   'prefixAttributeRecords': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/656ea1c5-1c18-4027-b688-b19d4f2cc78f',
}

attributeHex = {
   'shortAttributeRecord': '0x04',
   'attributeRecord': '0x05',
   'shortDictionaryAttributeRecord': '0x06',
   'dictionaryAttributeRecord': '0x07',
   'shortXmlnsAttributeRecord': '0x08',
   'xmlnsAttributeRecord': '0x09',
   'shortDictionaryXmlnsAttributeRecord': '0x0A',
   'DictionaryXmlsAttributeRecord': '0x0B',
   'PrefixDictionaryAttribute[A-Z]Records': '0x0C-0x25',
   'PrefixAttribute[A-Z]Records': '0x26-0x3F'
}

textLinks = {

   'zeroTextRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/407672b8-ecc9-4b32-83a2-731867a2fd66',
   'oneTextRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/5746d892-431e-4e34-b197-7d10c9255d98',
   'falseTextRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/cc7c8f96-80bb-49ef-abdd-61c6d2193342',
   'trueTextRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/25b6bb09-02e5-4d75-ae32-7a2f42ad77d9',
   'int8TextRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/ddd5ceb7-f36a-4a95-9e7c-78fea1137d2b',
   'int16TextRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/810f79bf-de9b-4869-a436-50bebe659ddc',
   'int32TextRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/edf56095-1dae-4a37-a628-1bc881ae0f10',
   'int64TextRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/77ace5e9-0767-4be0-b44c-2f78f36d137d',
   'floatTextRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/548c6211-c543-4969-b862-3698ee1f8b71',
   'doubleTextRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/4f10b50e-7152-4c28-8c3a-23cfe34eb6c2',
   'decimalTextRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/d419f393-2d40-49de-9901-adf8b35c19bf',
   'dateTimeTextRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/ee19ae39-f21d-4776-ada3-fb0f804b044c',
   'chars8TextRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/4d623c6e-d700-4091-a6b7-60e1d62a5c2a',
   'characterEscaping': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/6626d116-7a8d-4a7b-b75b-2eff4c25c596',
   'chars16TextRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/5bf3f11e-b201-465d-aefd-8456ba4e4bbc',
   'chars32TextRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/cd54178c-4c05-4015-9c33-4c1af139db79',
   'bytes8TextRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/17ffd2d9-dd35-4b99-9c59-bd551f91ab63',
   'bytes16TextRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/7546a7f1-d403-47ad-b625-c893e2543729',
   'bytes32TextRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/fcabae71-2662-4cbd-a1c7-07512a15f346',
   'startListText_endListTextRecords': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/4c4cf3f8-4e23-4687-b9c5-737ffee9440e',
   'emptyTextRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/e71526b7-5865-4daa-8b28-7d61fc42f681',
   'dictionaryTextRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/a41efc40-472a-420e-9d9f-bc9241dfcb26',
   'uniqueIdTextRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/1b79db81-8c1b-4db1-a7a0-46e70e0e8b4b',
   'timeSpanTextRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/f9b73b93-6974-43ae-9c4c-7b9f82f41b00',
   'uuidTextRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/576bc3c4-824b-4969-a0e7-79ec090abb8f',
   'uInt64TextRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/6ac58cba-b316-4f68-a6d5-4bf836ac7793',
   'boolTextRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/03802eb6-f76d-43a8-9cb3-8e2dd4d83f00',
   'unicodeChars8TextRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/107d1adf-63b3-4a6e-8b84-025f23817449',
   'unicodeChars16TextRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/7651e7f9-a22e-4825-b2bb-238c99ea0d2b',
   'unicodeChars32TextRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/e7e8f863-b593-48dd-8345-f9d23b0af2c8',
   'qNameDictionaryTextRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/1861dfa8-616c-40e5-b116-1fd7fd0f7ac0',
   'textWithEndElementRecords': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/da28ad87-2f06-479b-9ec5-01db9e80a4b1',
   
}

textHex = {
   'zeroTextRecord': '0x80',
   'oneTextRecord':  '0x82',
   'falseTextRecord': '0x84',
   'trueTextRecord': '0x86',
   'int8TextRecord': '0x88',
   'int16TextRecord': '0x8A',
   'int32TextRecord': '0x8C',
   'int64TextRecord': '0x8E',
   'floatTextRecord': '0x90',
   'doubleTextRecord': '0x92',
   'decimalTextRecord': '0x94',
   'dateTimeTextRecord': '0x96',
   'chars8TextRecord': '0x98',
   'characterEscaping': '0x99',
   'chars16TextRecord': '0x9A',
   'chars32TextRecord': '0x9C',
   'bytes8TextRecord': '0x9E',
   'bytes16TextRecord': '0xA0',
   'bytes32TextRecord': '0xA2',
   'startListTextRecords': '0xA4',
   'endListTextRecords': '0xA6',
   'emptyTextRecord': '0xA8',
   'dictionaryTextRecord': '0xAA',
   'uniqueIdTextRecord': '0xAC',
   'timeSpanTextRecord': '0xAE',
   'uuidTextRecord': '0xB0',
   'uInt64TextRecord': '0xB2',
   'boolTextRecord': '0xB4',
   'unicodeChars8TextRecord': '0xB6',
   'unicodeChars16TextRecord': '0xB8',
   'unicodeChars32TextRecord': '0xBA',
   'qNameDictionaryTextRecord': '0xBC',
   '*TextWithEndElementRecords': '0xBD'
}

# Miscellaneous Records

miscLinks = {
   'endElementRecord ': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/dba7ab5e-1789-42d7-acdd-6e4556b1553b',
   'commentRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/298c6768-9f19-46ed-a4e3-3f656655fe00',
   'arrayRecord': 'https://docs.microsoft.com/en-us/openspecs/windows_protocols/mc-nbfx/e0cd55a8-016d-4bb7-924e-a8b7add5d52b'
}


miscHex = {
   'endElementRecord': '0x01',
   'commentRecord': '0x02',
   'arrayRecord': '0x03'
}

# Code from the CLI

import requests
import bs4
from bs4 import BeautifulSoup
import pathlib
from pathlib import Path
import pandas as pd
import numpy as np
page = requests.get('url')
frames = pd.read_html(page.text)
