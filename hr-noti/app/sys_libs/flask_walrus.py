from walrus import Database

__all__ = ('WalrusDatabase')


class WalrusDatabase(object):
    """Flask extension class for walrus.Database."""

    def __init__(self, app=None, config_prefix=None):
        """Set config prefix and optionally initialize app configuration."""
        self.config_prefix = config_prefix or 'REDIS'

        if app is not None:
            self.init_app(app)

    def init_app(self, app):
        """Apply the Flask app configuration to a walrus.Database object."""
        self.app = app

        factory = self.config_get('FACTORY', Database)
        params = {}
        options = (
            'host',
            'port',
            'db',
            'password',
            'socket_timeout',
            'socket_connect_timeout',
            'socket_keepalive',
            'socket_keepalive_options',
            'decode_reponses',
            'encoding',
            'encoding_errors',
            'retry_on_timeout',
            'ssl',
            'ssl_keyfile',
            'ssl_certfile',
            'ssl_cert_reqs',
            'ssl_ca_certs'
        )
        for name in options:
            value = self.config_get(name)
            if value:
                params[name] = value

        self.database = factory(**params)

    def config_get(self, key, default=None):
        """Get app configuration value, taking prefix into account."""
        key = '{0}_{1}'.format(self.config_prefix, key.upper())
        return self.app.config.get(key, default)

    def __getattr__(self, name):
        """Make attributes from database instance available on extension."""
        if not name.startswith('_'):
            return getattr(self.__dict__['database'], name)
        else:
            raise AttributeError(name)