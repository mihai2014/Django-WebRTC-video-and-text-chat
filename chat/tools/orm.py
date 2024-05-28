# running django code outside the project

#BASE_DIR = "sigilari"

import platform, sys, os, django
from pathlib import Path

print(f"OS: {os.name}")
print(f"VERSION: {platform.system()} {platform.release()}")

path = Path(os.getcwd())
newpath = path.parent.parent
sys.path.append(str(newpath))
basedir = os.path.join(newpath, "interfon",)
sys.path.append(basedir)
print(sys.path)

#sys.path.append('/home/mihai/all/data/A_work/0/00_regio11/monitor')
# if platform.system() == "Windows":
#     sys.path.append('..\newsapi')
# if platform.system() == "Linux":
#     sys.path.append('../newsapi')

settings = 'config.settings'

#os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
os.environ['DJANGO_SETTINGS_MODULE'] = settings
#print(os.environ)

django.setup()


if __name__=="__main__":
    
    from django.conf import settings
    print(settings.BASE_DIR)

    #from app.models import Auto

    #ret = Auto.objects.all()
    #print(ret)