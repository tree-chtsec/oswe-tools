import pickle
import base64
import sys

pickle.loads(base64.b64decode(sys.argv[1].encode()))
