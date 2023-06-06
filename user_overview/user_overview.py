from genshi.builder import tag
from trac.core import Component, implements
from trac.util.html import html
from trac.wiki.macros import WikiMacroBase

class UserOverviewMacro(WikiMacroBase):
    _description = 'Displays a table of users and their associated details.'
    _domain = 'UserOverview'

    def expand_macro(self, formatter, name, content):
        # Database Connection
        db = self.env.get_read_db()

        # Query to get all user details
        cursor = db.cursor()
        cursor.execute("""
            SELECT s.sid, s.authenticated, a.name, a.value 
            FROM session AS s
            LEFT JOIN session_attribute AS a ON s.sid = a.sid
            WHERE s.authenticated = 1
        """)

        user_data = {}
        for sid, authenticated, attr_name, attr_value in cursor:
            if sid not in user_data:
                user_data[sid] = {'username': sid, 'cc_count': 0}

            if attr_name == 'name':
                user_data[sid]['full_name'] = attr_value
            elif attr_name == 'email':
                user_data[sid]['email'] = attr_value

        # Query to get cc entries for each ticket
        cursor.execute("""
            SELECT cc 
            FROM ticket 
            WHERE cc IS NOT NULL
        """)

        # Process the cc entries
        for cc_entries in cursor:
            for sid in cc_entries[0].split(','):
                sid = sid.strip()
                if sid in user_data:
                    user_data[sid]['cc_count'] += 1

        # Creating the table
        table = tag.table(class_="wiki")

        # Table Header
        table.append(tag.tr(
            tag.th('Username'),
            tag.th('Full Name'),
            tag.th('Email'),
            tag.th('Tickets CC\'d')
        ))

        # Table Data
        for user in sorted(user_data.values(), key=lambda x: x['cc_count'], reverse=True):
            table.append(tag.tr(
                tag.td(user['username']),
                tag.td(user.get('full_name', '')),
                tag.td(user.get('email', '')),
                tag.td(str(user['cc_count']))
            ))

        return table
