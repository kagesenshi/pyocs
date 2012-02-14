

class ActivityService(object):

    def __init__(self, store, personstore):
        """ accepts IActivityStorage """
        self.store = store
        self.personstore = personstore

    def listing(self, request, person_id):

        data = {
            'page': request.get('page', 0)
            'pagesize': request.get('pagesize', 20)
        }

        limit = int(data['pagesize'] or 0)
        offset = int(limit * (data['page'] or 0))
        activities = [
            a.data() for a in self.store.get_activities(
                            person_id, limit, offset)
        ]

        result = Result()

        data = []
        for activity in activities:
            data.append(Activity(**activity))

        if data:
            result.data = data
        return result

    def post_message(self, request, person_id):
        message = request.get('message', None)

        if message is None:
            return Result(False, 101, 'empty message')

        person = self.personstore.get_person(person_id)

        if person is None:
            return Result(False, 102, 'user not found')

        storage.store.add_activity(person_id, data)
        return Result()
