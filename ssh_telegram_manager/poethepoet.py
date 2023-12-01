from ssh_telegram_manager import __version__
from os import system

def pytest():
    system("pytest")
    
def coverage():
    system("coverage run -m pytest && coverage report && coverage html")

def translate():
        system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o ssh_telegram_manager/locale/ssh_telegram_manager.pot  ssh_telegram_manager/*.py ssh_telegram_manager/reusing/*.py ")
        system("msgmerge -N --no-wrap -U ssh_telegram_manager/locale/es.po ssh_telegram_manager/locale/ssh_telegram_manager.pot")
        system("msgfmt -cv -o ssh_telegram_manager/locale/es/LC_MESSAGES/ssh_telegram_manager.mo ssh_telegram_manager/locale/es.po")
        system("msgfmt -cv -o ssh_telegram_manager/locale/en/LC_MESSAGES/ssh_telegram_manager.mo ssh_telegram_manager/locale/en.po")

def release():
    print("""
    Nueva versión:
  * Cambiar la versión en ssh_telegram_manager/__init__.py
  * Cambiar la versión en pyproject.toml
  * Modificar el Changelog en README
  * poe coverage
  * poe translate
  * linguist
  * poe translate
  * git commit -a -m 'ssh_telegram_manager-{0}'
  * git push
  * Hacer un nuevo tag en GitHub
  * poetry build
  * poetry publish --username --password  
  * Crea un nuevo ebuild de ssh_telegram_manager Gentoo con la nueva versión
  * Subelo al repositorio del portage

""".format(__version__))

