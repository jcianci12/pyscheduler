from flask import Flask, jsonify, url_for, redirect
from authlib.integrations.flask_client import OAuth

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Set a secret key for Flask session

oauth = OAuth(app)

authentik = oauth.register(
    'authentik',
    client_id='yJwnySrODx2x1uNDKzszWiTV3ivrLPBdvvDkz1sN',
    client_secret='7hY48mDD1MCqW6irlkdvY61Vq1DiOPIVKCcpPxkAKn3un2JXyY6N2Knm0SHGOA2uzdo7zJQpz1ax3R6kxH6NWQyHJz6rKXodBJ2lqk9sQk6Y6pjaPkH1xFpoKrC3SeMd',
    access_token_url='https://authentik.tekonline.com.au/application/o/token/',
    authorize_url='https://authentik.tekonline.com.au/application/o/authorize/',
    api_base_url='https://authentik.tekonline.com.au/application',
    jwks_uri='https://authentik.tekonline.com.au/application/o/pyscheduler/jwks/',
    client_kwargs={'scope': 'openid read:users write:users email'},
    authorize_params={'response_type': 'code'}
)




