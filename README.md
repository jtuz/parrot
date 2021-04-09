# Puesta en marcha de el entorno de desarrollo

## Tabla de contenido.

* [Herramientas de desarrollo](#markdown-header-herramientas-de-desarrollo)
    * [Infraestructura](#markdown-header-infraestructura)
    * [Editor o IDE](#markdown-header-editor-o-ide)
    * [Markdown](#markdown-header-markdown)
    * [Convenciones de Git](#markdown-header-convenciones_de_git)
* [NOTA importante antes de empezar](#markdown-header-nota-importante-antes-de-empezar)
* [Proyecto Django](#markdown-header-proyecto-django)

## Herramientas de desarrollo.

### Infraestructura

Para reducir errores de compatibilidad entre el equipo de desarrollo se
necesita tener un entorno de desarrollo homogéneo y lo mas cercano a el entorno
de producción (punto 10 de [https://12factor.net/](https://12factor.net/)), por
lo que sera necesario descargar las siguientes herramientas y poner el entorno
de desarrollo en marcha.

1. [VirtualBox](https://www.virtualbox.org/wiki/Downloads)
2. [Vagrant](https://www.vagrantup.com/downloads)
3. Instalar el plugin `vagrant-vbguest` de la siguiente forma:

```sh
vagrant plugin install vagrant-vbguest
```

La compatibilidad de la versión de el lenguaje y librerías están definidas dentro
de el proyecto en el archivo `.python-version`, el entorno `virtualenv` viene
establecido e instalado automáticamente dentro de el aprovisionamiento de este
proyecto, para mas detalles puede consultar [Proyecto Django](#proyecto-django).

### Editor o IDE

Para una mejor integración y comunicación entre el equipo de desarrollo es
necesario establecer una guia de estilos al cual todos se apeguen con la
finalidad de establecer estándares de codificación que ayuden a una mejor
legibilidad y entendimiento de el código, debido a que la mayoría de el
proyecto esta basado en python, la guia de estilos elegida es la establecida
por la comunidad [PEP8](https://pep8.org/), sin embargo debido a que el
framework utilizado en el proyecto es Django, algunas reglas básicas se tienen
que ajustar dada la naturaleza de el framewok, para consultar los ajustes
ver [Django coding style](https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/coding-style/)
para lograr cumplir en la mayoría de lo posible con los estándares de
codificación se ha elegido dos herramientas para este propósito, dependiendo de
la preferencia de el desarrollador, ya sea que opte por usar un editor o un
IDE, es necesario instalar las herramientas mencionadas listadas a continuación
y realizar los ajustes necesarios dependiendo de la elección:

1. [EditorConfig](https://editorconfig.org/#download)
2. [Flake8](https://pypi.org/project/flake8/)

El proyecto incluye dos archivos que trae pre configurado las particularidades
de el proyecto que afectan a la guia de estilos, `.editorconfig` que trae todas
las reglas de indentación por tipo de archivo, espaciado, limite de columnas,
remover espacios al final de linea, tipo de fin de archivo, etc, y `setup.cfg`
que ayuda a controlar las particularidades de la guia de _PEP8_.

### Markdown

Para este proyecto las convenciones utilizadas para escribir Markdown son las
expuestas en esta guia: [README.md](https://bitbucket.org/tutorials/markdowndemo/src/master/README.md#markdown-header-code-and-syntax-highlighting)
a diferencia de repositorios como Github que tienen sus extensiones propias
para makrdown, para este proyecto se escribirá lo mas apegado a las
especificaciones originales de Markdown.

### Convenciones de Git

Para tener un historial de cambios bien documentado es importante definir la
forma en como se deben de guardar dichos cambios, para este proyecto se sugieren
los definidos en el siguiente documento:

[Convenciones para escribir commits](https://bitbucket.org/init8/dot-files/src/master/)


## NOTA importante antes de empezar.

El aprovisionamiento de scripts es automático al momento de el primer arranque
realizado con `vagrant up` si por alguna razón se requiere ejecutar el
aprovisionamiento de cada script por separado se debe tener en cuenta lo
siguiente: El aprovisionamiento se ejecuta en tres casos, el `vagrant up`
inicial, ejecutando directamente `vagrant provision` y `vagrant reload
--provision`.

El argumento `--provision-with <nombre_script>` se usa para ejecutar un script
en especifico de tal forma que para este proyecto las opciones disponibles son
las enumeradas a continuación.

1. Instalación básica, el aprovisionamiento se realiza ejecutando el comando y
   argumentos `vagrant provision --provision-with bootstrap`, la instalación
   considera:

   * Actualización de el sistema
   * Instalación de herramientas de desarrollo y compilación
   * Instalación de paquetes básicos
   * Instalación de Postgres 9.6
   * Instalación de Postgis 2.5
   * Instalación de `pyenv`
   * Instalación de Python 3.8.3
   * Instalación de entorno virtual python para el desarrollo de el proyecto

## Proyecto Django.

El script de aprovisionamiento inicial trata de instalar los requerimientos
iniciales de python necesarios para el proyecto, en caso de que no se haya
realizado, es posible ejecutar individualmente la instalación realizando los
pasos descritos a continuación.

```sh
vagrant ssh
cd /vagrant
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

Una vez instaladas todas las dependencias de el proyecto proceda a copiar el
archivo de ejemplo que esta dentro de el proyecto `.env.example` en el
directorio `core/settings` y renombre el archivo hacia `.env` es importante
que el archivo `.env` nunca sea añadido al repositorio, cualquier valor que
deba añadirse deberá ser manual o en su defecto compartirlo por un medio
seguro entre el equipo de desarrollo.

Para un entorno instalado desde cero es necesario crear ejecutar las tareas de
migración para la base de datos inicial y crear una cuenta de administrador 
para la aplicación de la siguiente forma, esto se ejecuta desde la
raíz de el proyecto (`/vagrant`) y dentro de el entorno virtual:

```sh
python manage.py migrate
python manage.py createsuperuser
```

En caso de que se este trabajando con un respaldo provisto por algún miembro de
el equipo, deberá consultar respecto a los datos de acceso previamente creados.

Para futuras ejecuciones de el servidor de desarrollo bastara con entrar a
vagrant y ejecutar de la siguiente forma (todo esto desde la raíz de el
proyecto que contiene el archivo `Vagrantfile`)

```sh
vagrant ssh
runserver
```
