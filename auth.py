from flask import Flask, jsonify, url_for, redirect
from authlib.integrations.flask_client import OAuth
from authlib.jose import jwt

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


@app.route('/')
def login():
    redirect_uri = url_for('authorize', _external=True)
    return authentik.authorize_redirect(redirect_uri)

@app.route('/authorize')
def authorize():
    token = authentik.authorize_access_token()
    user_info = authentik.get('https://authentik.tekonline.com.au/application/o/userinfo/', token=token)
    # decoded_token = jwt.decode(user_info, options={"verify_signature": False})
    return jsonify(user_info.text)

if __name__ == '__main__':
    app.run()


