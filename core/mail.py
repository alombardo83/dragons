from django.conf import settings
import django.core.mail


def get_connection(label=None, **kwargs):
    if label is None:
        label = getattr(settings, 'EMAIL_CONNECTION_DEFAULT', None)

    try:
        connections = getattr(settings, 'EMAIL_CONNECTIONS')
        options = connections[label]
    except KeyError:
        print('Settings for connection "%s" were not found' % label)

    options.update(kwargs)
    connection = django.core.mail.get_connection(**options)
    if not hasattr(connection, 'username'):
        connection.username = None
    return connection
