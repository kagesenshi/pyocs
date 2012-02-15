from pyocs import schema
from pyocs.base import make_object, Result

def Person(**data):
    return make_object(schema.IPerson, data)

def xml_decoder(data):
    data['privacy'] = int(data.get('privacy', 0))
    return Person(**data)

class PersonService(object):

    def __init__(self, store):
        """
            accepts IPersonStorage 
        """
        self.store = store

    def check(self, request):
        """
            accepts IRequest
        """
        login = request.get('login', None)
        login = request.get('login', None)
        password = request.get('password', None)

        if login is None:
            return Result(False, 101,
                'please specify all mandatory fields ')
 
        credentials = {
            'login': login,
            'password': password
        }

        if not self.store.authenticate(credentials):
            return Result(False, 102, 'login not valid')

        result = Result()

        result.data = [Person(personid=login)]
        return result

    def add(self, request):
        login = request.get('login', None)
        password = request.get('password', None)
        firstname = request.get('firstname', None)
        lastname = request.get('lastname', None)
        email = request.get('email', None)

        if not (login and password and firstname and lastname and email):
            return Result(False, 101, 'please specify all mandatory fields')

        if len(password) < 8:
            return Result(False, 102,
                        'please specify a password longer than 8 characters')

        if not re.match(r'^[A-Za-z0-9]{0,9999}$', login):
            return Result(False, 102,
                        'login can only consist of alphanumeric characters')

        if '@' not in email:
            # not sure whats the best email validator parser around
            return Result(False, 106, 'invalid email')

        if (self.store.get_person(login) or
            self.store.get_pending_person(login)):
            return Result(False, 104,
                '%s already taken, please choose a different login' % login)

        if self.store.get_person_by_email(email):
            return Result(False, 105,
                '%s already have an account associated' % email)

        self.store.send_email_verification(**{
            'login': login,
            'password': password,
            'firstname': firstname,
            'lastname': lastname,
            'email': email
        })

        return Result()


    def data(self, request, person_id):
        person = self.store.get_person(person_id)
        if not person:
            return Result(False, 101, 'unknown user id')

        if not person.viewable_by(request.current_user()):
            return Result(False, 102, 'user is private')

        result = Result()
        result.data = [
            Person(**person.get_properties())
        ]

        return result

    def self(self, request):
        person = self.store.get_person(request.current_user())
        result = Result()
        result.data = [
            Person(**person.get_properties())
        ]
        return result

    def set_self(self, request):

        data = {
            'latitude': request.get('latitude', None),
            'longitude': request.get('longitude', None),
            'city': request.get('city', None),
            'country': request.get('country', None)
        }

        has_param = False
        for key, value in data.items():
            if value != None:
                has_param = True
                break

        if not has_param:
            return Result(False, 101, 'No parameter to update found')

        person = self.store.get_person(request.current_user())

        person.set_properties(data)

        return result


    def balance(self, request):
        person = self.store.get_person(request.current_user())

        result = Result()
        result.data = [
            Person(**person.get_balance())
        ]

        return result

    def attributes(self, request, person_id, app=None, key=None):
        person = self.store.get_person(person_id)

        result = Result()

        data = person.get_xattr(app, key)
        if data:
            result.data = [
                Attribute(person.get_xattr(app, key))
            ]

        return result

    def setattribute(self, request, app, key):
        value = request.get('value', None)
        person = storage.get_person(request.current_user())

        person.set_xattr(app, key, value)

        return Result()

    def deleteattribute(self, request, app, key):
        person = storage.get_person(request.current_user())

        person.delete_xattr(app, key, value)

        return Result()
