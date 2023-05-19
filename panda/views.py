from django.shortcuts import render
from django.http import HttpResponseRedirect
from urllib.parse import quote_plus, urlencode
from os import environ as env
from dotenv import find_dotenv, load_dotenv

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
            },
            quote_via=quote_plus,
        )
    )

def callback(request):
    code = ''
    if 'code' in request.GET:
            code = request.GET.get('code')
    return render(request, 'callback.html')