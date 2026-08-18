import sys, base64, os
path = sys.argv[1]
os.makedirs(os.path.dirname(path), exist_ok=True)
open(path, 'wb').write(base64.b64decode(sys.argv[2]))
print('Wrote', path)
