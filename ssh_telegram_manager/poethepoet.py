from ssh_telegram_manager.reusing.github import download_from_github
from ssh_telegram_manager import __version__
from os import system
from sys import argv


def pytest():
    system("pytest")
    
def coverage():
    system("coverage run --omit='*/reusing/*,*uno.py' -m pytest && coverage report && coverage html")


def reusing():
    """
        Actualiza directorio reusing
        poe reusing
        poe reusing --local
    """   
    local=False
    if len(argv)==2 and argv[1]=="--local":
        local=True
        print("Update code in local without downloading was selected with --local")
    if local==False:
        download_from_github('turulomio','reusingcode','python/github.py', 'ssh_telegram_manager/reusing/')
        download_from_github('turulomio','reusingcode','python/file_functions.py', 'ssh_telegram_manager/reusing/')

def translate():
        system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o ssh_telegram_manager/locale/ssh_telegram_manager.pot  ssh_telegram_manager/*.py ssh_telegram_manager/reusing/*.py ")
        system("msgmerge -N --no-wrap -U ssh_telegram_manager/locale/es.po ssh_telegram_manager/locale/ssh_telegram_manager.pot")
        system("msgfmt -cv -o ssh_telegram_manager/locale/es/LC_MESSAGES/ssh_telegram_manager.mo ssh_telegram_manager/locale/es.po")
        system("msgfmt -cv -o ssh_telegram_manager/locale/en/LC_MESSAGES/ssh_telegram_manager.mo ssh_telegram_manager/locale/en.po")
        system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o locale/ssh_telegram_manager.pot *.py ssh_telegram_manager/*.py ssh_telegram_manager/reusing/*.py setup.py")
        system("msgmerge -N --no-wrap -U locale/es.po locale/ssh_telegram_manager.pot")
        system("msgfmt -cv -o ssh_telegram_manager/locale/es/LC_MESSAGES/ssh_telegram_manager.mo locale/es.po")
        system("msgfmt -cv -o ssh_telegram_manager/locale/en/LC_MESSAGES/ssh_telegram_manager.mo locale/en.po")



def release():
    print("""
    
            Nueva versión:
  * Cambiar la versión y la fecha en __init__.py
  * Modificar el Changelog en README
  * python setup.py translate
  * linguist
  * python setup.py translate
  * python setup.py uninstall; python setup.py install
  * python setup.py doxygen
  * git commit -a -m 'ssh_telegram_manager-{0}'
  * git push
  * Hacer un nuevo tag en GitHub
  * python setup.py sdist
  * twine upload dist/ssh_telegram_manager-{0}.tar.gz 
  * python setup.py uninstall
  * Crea un nuevo ebuild de ssh_telegram_manager Gentoo con la nueva versión
  * Subelo al repositorio del portage

    
    
    Nueva versión:
  * Cambiar la versión y la fecha en commons.py
  * Cambiar la versión en pyproject.toml
  * Modificar el Changelog en README
  * poe coverage
  * poe translate
  * linguist
  * poe translate
  * poe documentation
  * git commit -a -m 'ssh_telegram_manager-{0}'
  * git push
  * Hacer un nuevo tag en GitHub
  * poetry build
  * poetry publish --username --password  
  * Crea un nuevo ebuild de ssh_telegram_manager Gentoo con la nueva versión
  * Subelo al repositorio del portage

""".format(__version__))

