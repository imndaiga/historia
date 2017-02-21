from . import api
from flask_restful import Resource
from .decorators import requires_auth


class UserAPI(Resource):

    def get(self, id):
        return "Hello, World!"

    def put(self, id):
        pass

    def delete(self, id):
        pass


class pingAPI(Resource):
    decorators = [requires_auth]

    def get(self):
        return 'Here is a ping'

    def put(self):
        return 'Ping updated'

    def delete(self):
        return 'Ping deleted'

# relation_name:{value:'Father', type:'multiselect-input'},
# birth_date:{value:'2017-02-15', type:'pikaday-input'}


class relationshipsAPI(Resource):
    decorators = [requires_auth]

    def get(self):
        return [
            {
                'id': {'value': 1, 'type': 'hidden-input',
                       'input_name': 'data_id', 'label': 'ID'},
                'first_name': {'value': 'John', 'type': 'alpha-input',
                               'input_name': 'mod_first-name',
                               'label': 'First Name'},
                'ethnic_name': {'value': 'Mwaura', 'type': 'alpha-input',
                                'input_name': 'mod_ethnic-name',
                                'label': 'Ethnic Name'},
                'last_name': {'value': 'Ndungu', 'type': 'alpha-input',
                              'input_name': 'mod_last-name',
                              'label': 'Last Name'},
                'email': {'value': 'john.mwaura@gmail.com',
                          'type': 'email-input',
                          'input_name': 'mod_email',
                          'label': 'Email'}
            },
            {
                'id': {'value': 1, 'type': 'hidden-input',
                       'input_name': 'data_id', 'label': 'ID'},
                'first_name': {'value': 'Joanna', 'type': 'alpha-input',
                               'input_name': 'mod_first-name',
                               'label': 'First Name'},
                'ethnic_name': {'value': 'Moraa', 'type': 'alpha-input',
                                'input_name': 'mod_ethnic-name',
                                'label': 'Ethnic Name'},
                'last_name': {'value': 'Ndungu', 'type': 'alpha-input',
                              'input_name': 'mod_last-name',
                              'label': 'Last Name'},
                'email': {'value': 'joan.moraa@gmail.com',
                          'type': 'email-input',
                          'input_name': 'mod_email',
                          'label': 'Email'}
            },
            {
                'id': {'value': 1, 'type': 'hidden-input',
                       'input_name': 'data_id', 'label': 'ID'},
                'first_name': {'value': 'Jeremiah', 'type': 'alpha-input',
                               'input_name': 'mod_first-name',
                               'label': 'First Name'},
                'ethnic_name': {'value': 'Mugwe', 'type': 'alpha-input',
                                'input_name': 'mod_ethnic-name',
                                'label': 'Ethnic Name'},
                'last_name': {'value': 'Ndungu', 'type': 'alpha-input',
                              'input_name': 'mod_last-name',
                              'label': 'Last Name'},
                'email': {'value': 'jerendu@gmail.com',
                          'type': 'email-input',
                          'input_name': 'mod_email',
                          'label': 'Email'}
            }
        ]

    def put(self):
        return 'Relationship added'

    def delete(self):
        return 'Relationship deleted'


api.add_resource(relationshipsAPI, '/relationships', endpoint='relationships')
api.add_resource(pingAPI, '/ping', endpoint='ping')
api.add_resource(UserAPI, '/users/<int:id>', endpoint='user')
