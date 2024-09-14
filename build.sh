
#!/usr/bin/env bash
# exit on error
set -o errexit

pip freeze > requirements.txt
pip install -r requirements.txt
pip install gunicorn
