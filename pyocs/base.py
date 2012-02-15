from zope import schema
from zope.interface import directlyProvides
from pyocs import schema as ocsschema
import xmldict

_DECODERS={} # registry for functions which convert json/xml to OCSObject

def registerDecoder(format_, type_, func):
    """ Register a decoder """
    _DECODERS.setdefault(format_, {})
    _DECODERS[format_][type_] = func

def getDecoder(type_, format_):
    _DECODERS.setdefault(format_, {})
    result = _DECODERS[format_].get(type_, None)
    if result is None:
        raise Exception('No decoder found for %s %s' % (type_, format_))
    return result

class OCSObject(object):

    def __repr__(self):
        return '<pyocs.%s at %s>' % (self.__schema__.__name__,
                                    hex(id(self)))

def make_object(iface, data=None, baseclass=OCSObject):
    data = data or {}
    defaults = {}

    for key, value in schema.getFields(iface).items():
        if isinstance(value, schema.List):
            defaults.setdefault(key, [])
        else:
            defaults.setdefault(key, value.default)

    defaults.update(data)

    obj = baseclass()

    directlyProvides(obj, iface)

    obj.__schema__ = iface
    for key, value in defaults.items():
        setattr(obj, key, value)

    return obj


def Result(success=True, statuscode=100, message=''):
    if success:
        status = 'ok'
    else:
        status = 'failed'
    obj = make_object(ocsschema.IResult, {
        'status': status,
        'statuscode': statuscode,
        'message': message
    })
    return obj



def obj_from_result_xml(result):
    parsed = xmldict.xml_to_dict(result)
    status = True if parsed['ocs']['meta']['status'] == 'ok' else False
    r = Result(status, 
            int(parsed['ocs']['meta']['statuscode']),
            parsed['ocs']['meta']['message'])

    data = []
    for type_, values in parsed['ocs']['data'].items():
        convertor = getDecoder(type_, 'xml')
        if isinstance(values, list):
            for i in values:
                data.append(convertor(i))
        else:
            data.append(convertor(values))
    r.data = data
    return r
