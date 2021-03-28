# -*- coding: utf-8 -*-
from flask_script import Manager
from app.flask_app import create_app, configure_app, DEFAULT_GLOBAL_CONFIG_FILE
from app.extensions import db
from flask import url_for


# init Flask app
app = create_app()
manager = Manager(app)


# run api using Flask-Script
@manager.option('-c', '--config', dest='config_file', default=DEFAULT_GLOBAL_CONFIG_FILE)
def runserver(config_file):
    """Run in local machine."""
    configure_app(app, filename=config_file)

    if app.config.get("DEBUG"):
        print("debug mode")
        app.run(host='0.0.0.0', port=5001, use_reloader=False, threaded=True
                # ssl_context=(app.config.get("CERT_PEM"), app.config.get("KEY_PEM"))
                )
    else:
        print("runable mode")
        app.run(host='0.0.0.0', port=5001, use_reloader=False, threaded=True,
                # ssl_context=(app.config.get("CERT_PEM"), app.config.get("KEY_PEM"))
                )


@manager.command
def list_routes():
    import urllib
    output = []
    for rule in app.url_map.iter_rules():

        options = {}
        for arg in rule.arguments:
            options[arg] = "[{0}]".format(arg)

        methods = ','.join(rule.methods)
        url = url_for(rule.endpoint, **options)
        line = urllib.unquote("{:50s} {:20s} {}".format(rule.endpoint, methods, url))
        output.append(line)

    for line in sorted(output):
        print(line)


def createdb(app):
    """
    Initially create the tables in the database. The database must exist.
    (SQLite database will be created)
    """
    # configure_app(app, filename=DEFAULT_GLOBAL_CONFIG_FILE)
    with app.app_context():
        print(db)
        db.create_all()
        db.session.commit()


# run api using WSGI
def build_app(config_file=DEFAULT_GLOBAL_CONFIG_FILE):
    configure_app(app, filename=config_file)
    return app


if __name__ == "__main__":
    import os
    os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
    manager.run(default_command='runserver')
