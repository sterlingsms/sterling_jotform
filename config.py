import os

# Enable Development Env

DEBUG = True

# Application Directory

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

# Application threads. Common assumption is
# to use 2 threads per available core.
# Handles incoming requests using one and 
# performs background operations on other.

THREADS_PER_PAGE = 2

# CSRF

CSRF_ENABLED = True
CSRF_SESSION_KEY = ''

# Key for cookies

SECRET_KEY = 'Same as Session Key'

# define your API key and the form ID
JOTFORM_EP_BASE_URL = 'https://input.sterlingadministration.com/'
JOTFORM_API_BASE_TEAM_URL = 'https://input.sterlingadministration.com/API/team/230545034230038'
API_KEY = '94f27c41cc7a995b889f29006c6ff2e7'
TEAM_ID = '230545034230038'

# Medication Log : Form ID

MEDI_FORM_ID = '223625492681057'

# Lab Order Form : Form ID 
# BUP 231364985876069 order colloection form

OC_FORM_ID = '231925455272963'
OC_REQUEST_FORM_ID = '231296684863065'
OC_PROVIDER_REGISTER_FORM_ID = '231925353092051'

# site URL
OC_REQUEST_FORM_SS="https://oclabs.sterlingadministration.com/oc-lab-request?sid="
