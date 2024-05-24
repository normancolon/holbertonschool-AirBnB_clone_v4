#!/usr/bin/python3
"""Flask Application"""
from flask import Flask, render_template, make_response, jsonify
from flask_cors import CORS
from flasgger import Swagger
from os import environ
from models import storage
from api.v1.views import app_views

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Register blueprint
app.register_blueprint(app_views)

# Enable CORS for API
cors = CORS(app, resources={r"/api/v1/*": {"origins": "*"}})

@app.teardown_appcontext
def close_db(error):
    """Close Storage"""
    storage.close()

@app.errorhandler(404)
def not_found(error):
    """404 Error handler
    ---
    responses:
      404:
        description: A resource was not found
    """
    return make_response(jsonify({'error': "Not found"}), 404)

# Swagger configuration
app.config['SWAGGER'] = {
    'title': 'AirBnB clone Restful API',
    'uiversion': 3
}
Swagger(app)

def get_env_variable(var_name, default_value):
    """Helper function to get environment variables"""
    return environ.get(var_name, default_value)

if __name__ == "__main__":
    """Main Function"""
    host = get_env_variable('HBNB_API_HOST', '0.0.0.0')
    port = get_env_variable('HBNB_API_PORT', '5000')
    app.run(host=host, port=port, threaded=True)
