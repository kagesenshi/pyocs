from zope.interface import Interface

class IStorage(Interface):
    pass

class IPersonStorage(IStorage):
    def add_person(login, password, firstname, lastname, email):
        """ return object which implements IPerson """

    def get_person(login):
        """ return object which implements IPerson """

    def get_person_by_email(email):
        """ return object which implements IPerson """

    def get_person_by_apikey(apikey):
        """ return object which implements IPerson """

class IActivityStorage(IStorage):

    def add_activity(person_id, data, timestamp=None):
        """
            Add activity stream item. if timestamp is None, use current utc
            datetime
        """

    def get_activities(person_id, limit=None, offset=None):
        """
            return list of IActivity.
        """
