import pyocs
from pyocs.base import obj_from_result_xml
from pyocs import schema

def test_person_from_xml():
    xml = '''<?xml version="1.0"?>
<ocs>
 <meta>
  <status>ok</status>
  <statuscode>100</statuscode>
  <message></message>
 </meta>
 <data>
  <person details="check">
   <personid>frank</personid>
  </person>
 </data>
</ocs>'''
    r = obj_from_result_xml(xml)
    assert schema.IResult.providedBy(r)
    for i in r.data:
        assert schema.IPerson.providedBy(i)
    assert r.data[0].personid == 'frank'
    assert r.status == 'ok'
    assert r.statuscode == 100

    xml = '''<ocs>
 <meta>
  <status>ok</status>
  <statuscode>100</statuscode>
  <message></message>
  <totalitems>2</totalitems>
  <itemsperpage>10</itemsperpage>
 </meta>
 <data>
  <person details="summary">
   <personid>Testy</personid>
   <privacy>0</privacy>
   <privacytext>public</privacytext>
   <firstname>Peter</firstname>
   <lastname>-</lastname>
   <company></company>
   <gender></gender>
   <communityrole></communityrole>
   <city>London</city>
   <country></country>
  </person>
  <person details="summary">
   <personid>peter</personid>
   <privacy>0</privacy>
   <privacytext>public</privacytext>
   <firstname>Frank</firstname>
   <lastname>Test</lastname>
   <company>company</company>
   <gender>male</gender>
   <communityrole></communityrole>
   <city>London</city>
   <country></country>
  </person>
 </data>
</ocs>'''
    r = obj_from_result_xml(xml)
    assert schema.IResult.providedBy(r)
    for i in r.data:
        assert schema.IPerson.providedBy(i)
    assert r.data[0].privacy == 0
    assert r.data[0].privacytext == 'public'
    assert r.data[0].firstname == 'Peter'
    assert r.data[0].city == 'London'
    assert r.data[1].personid == 'peter'
    assert r.data[1].gender == 'male'
