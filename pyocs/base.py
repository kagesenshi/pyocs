from zope import schema
from zope.interface import directlyProvides
from pyocs import schema as ocschema

class OCSObject(object):

    def __repr__(self):
        return '<pyocs.%s at %s>' % (self.__schema__.__name__,
                                    hex(id(self)))

def make_object(iface, data=None, baseclass=Object):
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

