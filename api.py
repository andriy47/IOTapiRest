from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

TODOS = {
    'coche1': {
                'speed': 70,
                'engine': 'stop',
                'sensor':'disable',
                'status': 'Stopped',
            },
    'coche2': {
                'speed': 30,
                'engine': 'stop',
                'sensor':'disable',
                'status': 'Stopped',
            },
    'coche3': {
                'speed': 10,
                'engine': 'stop',
                'sensor':'disable',
                'status': 'Stopped',
            },
    'coche4': {
                'speed': 0,
                'engine': 'forward',
                'sensor':'disable',
                'status': 'Stopped',
            }
    
}


def abort_if_todo_doesnt_exist(coche_id):
    if coche_id not in TODOS:
        abort(404, message="Conohe {} doesn't exist".format(coche_id))

parser = reqparse.RequestParser() 
parser.add_argument('engine')
parser.add_argument('sensor')
parser.add_argument('speed')
parser.add_argument('status') 



class Todo(Resource):
    def get(self, coche_id):
        abort_if_todo_doesnt_exist(coche_id)
        return TODOS[coche_id]



    def delete(self, coche_id): 
        abort_if_todo_doesnt_exist(coche_id)
        del TODOS[coche_id]
        return 'Realizado con exito.', 204




    def put(self, coche_id): 
        args = parser.parse_args()
        TODOS[coche_id] = {'engine': args['engine'],'sensor': args['sensor'],'speed': args['speed'],'status': args['status']}
        return 'Ralizado con exito.', 201


# TodoList
# shows a list of all todos, and lets you POST to add new tasks
class TodoList(Resource):
    def get(self):
        return TODOS

    def post(self):
        args = parser.parse_args()
        coche_id = int(max(TODOS.keys()).lstrip('coche')) + 1
        coche_id = 'coche%i' % coche_id 
        TODOS[coche_id] = {'engine': args['engine'],'sensor': args['sensor'],'speed': args['speed'],'status': args['status']}
        
        return TODOS[coche_id], 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/coches')
api.add_resource(Todo, '/coches/<coche_id>')

if __name__ == '__main__':
    app.run(debug=True, port=5000)