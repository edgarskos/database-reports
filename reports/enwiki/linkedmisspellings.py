# Public domain; MZMcBride, Tim Landscheidt; 2012, 2013

"""
Report class for linked misspellings
"""

import reports

class report(reports.report):
    def get_title(self):
        return 'Linked misspellings'

    def get_preamble_template(self):
        return u'Linked misspellings (limited to the first 1000 entries); data as of <onlyinclude>%s</onlyinclude>.'

    def get_table_columns(self):
        return ['Article', 'Incoming links']

    def get_table_rows(self, conn):
        cursor = conn.cursor()
        cursor.execute('''
        /* linkedmisspellings.py SLOW_OK */
        SELECT
          CONVERT(p1.page_title USING utf8),
          COUNT(*)
        FROM page AS p1
        JOIN categorylinks
        ON p1.page_id = cl_from
        JOIN pagelinks
        ON p1.page_title = pl_title AND pl_namespace = 0
        JOIN page AS p2
        ON pl_from = p2.page_id AND p2.page_namespace = 0
        WHERE p1.page_namespace = 0
        AND p1.page_is_redirect = 1
        AND cl_to = 'Redirects_from_misspellings'
        GROUP BY 1
        LIMIT 1000;
        ''')

        for misspelled_redirect, incoming_links in cursor:
            yield ['{{dbr link|1=%s}}' % misspelled_redirect, str(incoming_links)]

        cursor.close()
