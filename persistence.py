import psycopg2
import psycopg2.extras
import os
from urllib import parse


def get_connection_string():
    user_name = os.environ.get('PSQL_USER_NAME')
    password = os.environ.get('PSQL_PASSWORD')
    host = os.environ.get('PSQL_HOST')
    database_name = os.environ.get('PSQL_DB_NAME')

    env_variables_defined = user_name and password and host and database_name

    if env_variables_defined:
        return 'postgresql://{user_name}:{password}@{host}/{database_name}'.format(
            user_name=user_name,
            password=password,
            host=host,
            database_name=database_name
        )
    else:
        raise KeyError('Some necessary environment variable(s) are not defined')


def open_database():

    current_env = 'DEV'

    if current_env == 'DEV':
        try:
            connection_string = get_connection_string()
            connection = psycopg2.connect(connection_string)
            connection.autocommit = True
        except psycopg2.DatabaseError as exception:
            print('Database connection problem')
            raise exception
        return connection
    else:
        parse.uses_netloc.append('postgres')
        url = parse.urlparse(os.environ.get('DATABASE_URL'))
        connection = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        return connection


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        connection.close()
        return ret_value

    return wrapper


_cache = {}


@connection_handler
def _retrieve_from_db(cursor, table):

    cursor.execute(f'SELECT * FROM {table}')
    data = cursor.fetchall()
    return data


def _get_data(data_type, table, force):

    if force or data_type not in _cache:
        _cache[data_type] = _retrieve_from_db(table)
    return _cache[data_type]


def clear_cache():
    for k in list(_cache.keys()):
        _cache.pop(k)


def get_statuses(force=False):
    return _get_data('statuses', 'status', force)


def get_boards(force=False):
    return _get_data('boards', 'board', force)


def get_cards(force=False):
    return _get_data('cards', 'card', force)
