# coding=utf-8
from django.db import connection
from django.template import Template, Context


def print_sql():
    if connection.queries:
        time = sum([float(q['time']) for q in connection.queries])
        t = Template(
            "{{count}} quer{{count|pluralize:\"y,ies\"}} in {{time}} seconds:\n{% for sql in sqllog %}[{{forloop.counter}}] {{sql.time}}s: {{sql.sql|safe}}{% if not forloop.last %}\n{% endif %}{% endfor %}")
        print t.render(Context({'sqllog': connection.queries, 'count': len(connection.queries), 'time': time}))


def clear_sql():
    connection.queries = []