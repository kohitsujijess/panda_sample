from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect
from urllib.parse import quote_plus, urlencode
from os import environ as env
from dotenv import find_dotenv, load_dotenv
import requests
import base64
import json

ENV_FILE = find_dotenv()
if ENV_FILE:
    load_dotenv(ENV_FILE)

def index(request):
    return render(request, 'index.html')

def login(request):
    redirect_uri = 'http://localhost:8000/panda/callback'
    return HttpResponseRedirect(
        'https://' + env.get('AUTH0_DOMAIN')
        + '/authorize?'
        + urlencode(
            {
                'response_type': 'code',
                'client_id': env.get('AUTH0_CLIENT_ID'),
                'redirect_uri': redirect_uri,
                'scope': 'openid%20profile',
                'state': 'xyzABC123',
                'audience': 'https://' + env.get('AUTH0_DOMAIN') + '/api/v2/',
            },
            quote_via=quote_plus,
        )
    )

def callback(request):
    code = ''
    redirect_uri = 'http://localhost:8000/panda/callback2'
    if 'code' in request.GET:
        code = request.GET.get('code')
    url = 'https://' + env.get('AUTH0_DOMAIN') + '/oauth/token'
    payload = urlencode(
        {
            'grant_type': 'authorization_code',
            'client_id': env.get('AUTH0_CLIENT_ID'),
            'client_secret': env.get('AUTH0_CLIENT_SECRET'),
            'code': code,
            'redirect_uri': redirect_uri,
        },
        quote_via=quote_plus,
    )

    headers = { 'content-type': "application/x-www-form-urlencoded" }
    params = {'payload': payload}
    response = requests.post(url, payload, headers=headers)
    data = json.loads(response.text)['access_token'].split('.')
    header = json.loads(base64.urlsafe_b64decode(data[0] + '=' * (-len(data[0]) % 4)).decode())
    payload = json.loads(base64.urlsafe_b64decode(data[1] + '=' * (-len(data[1]) % 4)).decode())
    params = {
        'text': '',
        'status': response.status_code,
        'header': header,
        'payload': payload,
    }
    return render(request, 'callback.html', params)


def callback2(request):
    return render(request, 'callback.html')

def logout(request):
    request.session.clear()

    return redirect(
        f"https://{env.get('AUTH0_DOMAIN')}/v2/logout?"
        + urlencode(
            {
                'returnTo': 'http://localhost:8000/panda',
                'client_id': env.get('AUTH0_CLIENT_ID'),
            },
            quote_via=quote_plus,
        ),
    )
