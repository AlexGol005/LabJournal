from django.core.management.utils import get_random_secret_key
get_random_secret_key()
print(get_random_secret_key())
# pip freeze > requirements.txt
# pip install -r requirements.txt
# cp template.env .env

# import os
# from pathlib import Path
# from dotenv import load_dotenv
# load_dotenv()

# SECRET_KEY = os.getenv('SECRET_KEY')
# DEBUG = os.getenv('DEBUG') == 'true'
# ALLOWED_HOSTS = [host.strip() for host in os.getenv('ALLOWED_HOSTS').split(',')]

# SECRET_KEY = "(d$$n4g3ipi+$$*(!h4zljt14hrr*=h5o^m(n88)s-l+e8ugxt"
# DEBUG = True
# ALLOWED_HOSTS = []

# SECRET_KEY = "vs3umg+heg!)ljfeg2o^eu@3fk1ma!=ett2^9o2x8cwjl@0ixy"
# DEBUG = True
# ALLOWED_HOSTS = "*"