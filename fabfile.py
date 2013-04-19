from fabric.api import run, env, cd


env.hosts = ['23.23.150.127', ]
env.user = 'ubuntu'
env.key_filename = ['~/.ssh/pineapple.pem', ]
env.port = '6969'
env.path = '/home/ubuntu/ranqus/ranqus'


def deploy():
    pull()
    update_requirements()
    reload_supervisor()


def pull():
    with cd('~/ranqus/ranqus'):
        run('git checkout master')
        result = run('git pull origin master')
        print result


def update_requirements():
    with cd(env.path):
        result = run('~/ranqus/venv/bin/pip install -r requirements.txt')
        print result


def reload_supervisor():
    run('sudo supervisorctl stop ranqus:ranqus_gunicorn')
    run('sudo supervisorctl start ranqus:ranqus_gunicorn')
