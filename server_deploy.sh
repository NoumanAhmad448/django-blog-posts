source /opt/python-venv/test-django3/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt

python manage.py migrate