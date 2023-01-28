from setuptools import setup, Command
import site
import os
import platform

class Reusing(Command):
    description = "Fetch remote modules"
    user_options = [
      # The format is (long option, short option, description).
      ( 'local', None, 'Update files without internet'),
  ]

    def initialize_options(self):
        self.local=False

    def finalize_options(self):
        pass

    def run(self):
        from sys import path
        path.append("ssh_telegram_manager/reusing")
        if self.local is False:
            from github import download_from_github
            download_from_github('turulomio','reusingcode','python/github.py', 'ssh_telegram_manager/reusing/')
            download_from_github('turulomio','reusingcode','python/datetime_functions.py', 'ssh_telegram_manager/reusing/')
            download_from_github('turulomio','reusingcode','python/file_functions.py', 'ssh_telegram_manager/reusing/')

## Class to define doc command
class Translate(Command):
    description = "Update translations"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        #es
        os.system("xgettext -L Python --no-wrap --no-location --from-code='UTF-8' -o locale/ssh_telegram_manager.pot *.py ssh_telegram_manager/*.py ssh_telegram_manager/reusing/*.py setup.py")
        os.system("msgmerge -N --no-wrap -U locale/es.po locale/ssh_telegram_manager.pot")
        os.system("msgfmt -cv -o ssh_telegram_manager/locale/es/LC_MESSAGES/ssh_telegram_manager.mo locale/es.po")
        os.system("msgfmt -cv -o ssh_telegram_manager/locale/en/LC_MESSAGES/ssh_telegram_manager.mo locale/en.po")

    
class Procedure(Command):
    description = "Show release procedure"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        print("""Nueva versión:
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

""".format(__version__))


## Class to define doxygen command
class Doxygen(Command):
    description = "Create/update doxygen documentation in doc/html"

    user_options = [
      # The format is (long option, short option, description).
      ( 'user=', None, 'Remote ssh user'),
      ( 'directory=', None, 'Remote ssh path'),
      ( 'port=', None, 'Remote ssh port'),
      ( 'server=', None, 'Remote ssh server'),
  ]

    def initialize_options(self):
        self.user="root"
        self.directory="/var/www/html/doxygen/ssh_telegram_manager/"
        self.port=22
        self.server="127.0.0.1"

    def finalize_options(self):
        pass

    def run(self):
        print("Creating Doxygen Documentation")
        os.system("""sed -i -e "41d" doc/Doxyfile""")#Delete line 41
        os.system("""sed -i -e "41iPROJECT_NUMBER         = {}" doc/Doxyfile""".format(__version__))#Insert line 41
        os.system("rm -Rf build")
        os.chdir("doc")
        os.system("doxygen Doxyfile")      
        command=f"""rsync -avzP -e 'ssh -l {self.user} -p {self.port} ' html/ {self.server}:{self.directory} --delete-after"""
        print(command)
        os.system(command)
        os.chdir("..")

## Class to define uninstall command
class Uninstall(Command):
    description = "Uninstall installed files with install"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        if platform.system()=="Linux":
            os.system("rm -Rf {}/ssh_telegram_manager*".format(site.getsitepackages()[0]))
            os.system("rm /usr/bin/ssh_telegram_manager*")
        else:
            os.system("pip uninstall ssh_telegram_manager")

########################################################################

## Version of ssh_telegram_manager captured from commons to avoid problems with package dependencies
__version__= None
with open('ssh_telegram_manager/__init__.py', encoding='utf-8') as f:
    for line in f.readlines():
        if line.find("__version__ =")!=-1:
            __version__=line.split("'")[1]


setup(name='ssh_telegram_manager',
     version=__version__,
     description='Python app to log in Telegram ssh logins',
     long_description='Project web page is in https://github.com/turulomio/ssh_telegram_manager',
     long_description_content_type='text/markdown',
     classifiers=['Development Status :: 4 - Beta',
                  'Intended Audience :: Developers',
                  'Topic :: Software Development :: Build Tools',
                  'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
                  'Programming Language :: Python :: 3',
                 ], 
     keywords='ssh telegram advice logs',
     url='https://github.com/turulomio/ssh_telegram_manager',
     author='Turulomio',
     author_email='turulomio@yahoo.es',
     license='GPL-3',
     packages=[
        'ssh_telegram_manager', 
        'ssh_telegram_manager.reusing', 
        'ssh_telegram_manager.locale.es.LC_MESSAGES', 
        'ssh_telegram_manager.locale.en.LC_MESSAGES', 
    ],
     install_requires=['python-telegram-bot'],
     entry_points = {'console_scripts': [
                            'ssh_telegram_manager=ssh_telegram_manager.core:main',
                        ],
                    },
     cmdclass={'doxygen': Doxygen,
               'uninstall':Uninstall, 
               'translate': Translate,
               'procedure': Procedure,
               'reusing': Reusing,
              },
     zip_safe=False,
     include_package_data=True
)
