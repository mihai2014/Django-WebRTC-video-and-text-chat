This is a text and video chat using WebSockets for signallig and WebRTC for p2p video connection with Django support



Steps for installing:

- create python virtual environment
- create superuser 
  python manage.py shell
  python manage.py createsuperuser
  ...
- create users in admin interface
- it is required to use https
- for development testing, use go_ssl2_test.sh


Note: p2p works good for two users for the now one, if multiple users peers want to connect the same time, possible error 
