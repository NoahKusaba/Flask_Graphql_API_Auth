from flask import request, jsonify
from flask_graphql import GraphQLView
from graphql_setup import schema, app
import time 

t, token = 0, 'invalid' # Variables to track keys

def auth_required(fn):
    def wrapper(*args, **kwargs):
        session = request.headers.get('AUTH-HEADER')
        elapsed_time = time.perf_counter() - t
         # If token valid, return data
        if token != 'invalid' and session == token and elapsed_time < 60:  return fn(*args, **kwargs)
        else: return jsonify({'message':'Failed'}), 401  # Bad keys or timeout.
    return wrapper

def graphql_view():
    view =GraphQLView.as_view(
    'graphql',
    schema=schema,
    graphiql=True # for having the GraphiQL interface
)
    return auth_required(view)

# Generates token that will timeout after 60 seconds.
"""
- Real implementation would require login headers for token generation
- Also would store as a {token : initial_time} dictionary in a set() variable, would clear old tokens. 
"""
@app.route('/token')
def generate_token():
    global t, token
    t = time.perf_counter()  # reset counter, to accept new hash token
    token = str(hash(t))
    return jsonify({'AUTH-HEADER':token})

# Routes
app.add_url_rule(
    '/graphql-Auth',
    view_func = graphql_view()
)

if __name__ == '__main__':
    app.run(host = "0.0.0.0")


