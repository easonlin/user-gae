run:
	dev_appserver.py app.yaml	
flask:
	pip install flask
flask_oauth:
	pip install flask_oauth
install:
	cp supervisord-gae.ini /etc/supervisord.d
