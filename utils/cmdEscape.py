import re
import sys

data = sys.stdin.read()
data = re.sub(r'([\^\|\&\\\<\>])', r'^\1', data)
print(data)
