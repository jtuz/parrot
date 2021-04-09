#!/usr/bin/env bash
#############################################################
# This is a script to perform basic Server Setup for Centos 7
# we use these things on every server (last stable version):
# - pyenv + pyenv-virtualenv + python PYTHON_VERSION
# - Postgresql PG_VERSION
#############################################################

PG_VERSION=9.6
PYTHON_VERSION=3.8.3
PG_PACKAGE_VER=$(echo ${PG_VERSION}|tr -d '\.')

export PG_PSW='development'

# Update the CentOS
yum -y update
yum -y install yum-utils epel-release bzip2-devel.x86_64 readline-devel.x86_64\
               openssl-devel.x86_64 sqlite-devel.x86_64 libffi-devel.x86_64
yum -y groups install "Development Tools"

# USEFUL packages
yum -y install which wget vim

# Install PostgreSQL repository
rpm -Uvh https://download.postgresql.org/pub/repos/yum/${PG_VERSION}/redhat/rhel-7-x86_64/pgdg-redhat-repo-latest.noarch.rpm

# Install PostgreSQL Server
yum install -y postgresql${PG_PACKAGE_VER}-server\
               postgresql${PG_PACKAGE_VER}\
               postgresql${PG_PACKAGE_VER}-devel\
               postgis25_${PG_PACKAGE_VER}.x86_64

# Initialize database template
runuser -l postgres -c "/usr/pgsql-${PG_VERSION}/bin/initdb -D /var/lib/pgsql/${PG_VERSION}/data"

# Now finally start the PostgreSQL database by issuing the below command:
systemctl start postgresql-${PG_VERSION}.service
systemctl enable postgresql-${PG_VERSION}.service
service postgresql-${PG_VERSION} status

echo -e "${PG_PSW}\n${PG_PSW}" | passwd postgres

# Put PG_PSW in bashrc for postgres $HOME
export PG_HOME=$( getent passwd postgres  | cut -d: -f6 )
echo -e "alias MYPSW=${PG_PSW}" >> $PG_HOME/.bashrc

sudo -u postgres psql -c "ALTER USER postgres PASSWORD '${PG_PSW}';"
sudo -u postgres psql -c "CREATE ROLE noys WITH LOGIN CREATEDB PASSWORD '${PG_PSW}';"
sudo -u postgres psql -c "CREATE DATABASE noys OWNER noys;"

# Add password to pgpass as postgres
su postgres -c "echo \"*:*:*:postgres:${PG_PSW}\" >> ${PG_HOME}/.pgpass"
chmod 0600 ${PG_HOME}/.pgpass

# Install pyenv tool
runuser -l vagrant -c "curl https://pyenv.run | bash"
su vagrant -c "echo 'export PYENV_ROOT=\$HOME/.pyenv' >> ~/.bash_profile"
su vagrant -c "echo 'export PATH=\$PYENV_ROOT/bin:\$PATH' >> ~/.bash_profile"
su vagrant -c "echo 'eval \"\$(pyenv init -)\"' >> ~/.bash_profile"
su vagrant -c "echo 'eval \"\$(pyenv virtualenv-init -)\"' >> ~/.bash_profile"

# create some alias 
su vagrant -c "echo 'export PATH=/usr/pgsql-${PG_VERSION}/bin:\$PATH' >> ~/.bash_profile"
su vagrant -c "echo 'alias runserver=\"cd /vagrant && source /vagrant/venv/bin/activate && python manage.py runserver 0.0.0.0:8000\"' >> ~/.bash_profile"

# Install project dependencies
runuser -l vagrant -c "exec \$SHELL"
runuser -l vagrant -c "pyenv update"
runuser -l vagrant -c "pyenv install ${PYTHON_VERSION}"
runuser -l vagrant -c "cd /vagrant && python -m venv --system-site-packages venv"
# runuser -l vagrant -c "cd /vagrant && source venv/bin/activate && pip install --upgrade pip"
runuser -l vagrant -c "cd /vagrant && source venv/bin/activate && pip install -r requirements.txt"
runuser -l vagrant -c "cd /vagrant && source venv/bin/activate && pip install -r requirements-dev.txt"
