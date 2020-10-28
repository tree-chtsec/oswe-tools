import sys

def toDecimal(ip):
    segs = ip.split('.')
    _sum = 0
    for i, seg in enumerate(segs):
        _sum *= 256
        _sum += int(seg)
    return _sum

def toHex(ip):
    dv = toDecimal(ip)
    return hex(dv)

def toOct(ip):
    dv = toDecimal(ip)
    return oct(dv)

if __name__ == '__main__':
    ip = sys.argv[1]
    assert len(ip.split('.')) == 4
    print(toDecimal(ip))
    print(toHex(ip))
    print(toOct(ip))
