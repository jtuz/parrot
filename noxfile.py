import nox


@nox.session
def lint(session):
    session.install("flake8")
    session.run('flake8', './core')
    #  session.run('flake8', '--exclude=migrations', './noys_auth')


@nox.session
def run_test(session):
    session.install('-r', 'requirements.txt')
    session.run(
        'python', 'manage.py', 'test',
        env={
            'DJANGO_SETTINGS_MODULE': 'core.settings.test'
        }
    )
