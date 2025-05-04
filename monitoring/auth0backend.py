import requests
from social_core.backends.oauth import BaseOAuth2

class Auth0(BaseOAuth2):
    """Auth0 OAuth authentication backend"""
    name = 'auth0'
    SCOPE_SEPARATOR = ' '
    ACCESS_TOKEN_METHOD = 'POST'
    EXTRA_DATA = [
        ('picture', 'picture')
    ]

    def authorization_url(self):
        return "https://" + self.setting('DOMAIN') + "/authorize"

    def access_token_url(self):
        return "https://" + self.setting('DOMAIN') + "/oauth/token"

    def get_user_id(self, details, response):
        return details['user_id']

    def get_user_details(self, response):
        url = 'https://' + self.setting('DOMAIN') + '/userinfo'
        headers = {'authorization': 'Bearer ' + response['access_token']}
        resp = requests.get(url, headers=headers)
        userinfo = resp.json()
        return {
            'username': userinfo['nickname'],
            'first_name': userinfo.get('name', ''),
            'picture': userinfo.get('picture', ''),
            'user_id': userinfo['sub']
        }

def get_management_token():
    url = "https://dev-z5pfxhgu4mfs7iq8.us.auth0.com/oauth/token"
    payload = {
        "client_id": "IlgibyNesZOmi4gtWxTWrkMNJowtpv5x",
        "client_secret": "XWwgXvr624aXepaVB21FHIXAGjSTBgNM4-FbsvBeGWEcxsf3uAHHkoYxMbyJeFHl",
        "audience": "https://dev-z5pfxhgu4mfs7iq8.us.auth0.com/api/v2/",
        "grant_type": "client_credentials"
    }
    res = requests.post(url, json=payload)
    res.raise_for_status()
    return res.json()["access_token"]

def getRole(request):
    user = request.user
    auth0user = user.social_auth.filter(provider="auth0")[0]
    user_id = auth0user.uid 

    mgmt_token = get_management_token()

    url = f"https://dev-z5pfxhgu4mfs7iq8.us.auth0.com/api/v2/users/{user_id}/roles"
    headers = {
        'Authorization': f'Bearer {mgmt_token}'
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()
    roles = response.json()

    if roles and isinstance(roles, list):
        return roles[0]["name"] 
    return None