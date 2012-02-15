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
    ooooo = r.data
