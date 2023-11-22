from invoke import task

@task
def start(ctx):
    ctx.run("python manage.py runserver")

@task
def migrate(ctx):
    ctx.run("python manage.py makemigrations")
    ctx.run("python manage.py migrate")

@task
def populate(ctx):
    ctx.run("python config/populate_official.py")

@task
def pwpopulate(ctx):
    ctx.run("python config/populate.py")

@task
def coverage(ctx):
    ctx.run("coverage run --source='.' manage.py test ilmoweb")
    ctx.run("coverage html")

@task
def unittest(ctx):
    ctx.run("python manage.py test ilmoweb")

@task
def lint(ctx):
    ctx.run("pylint ilmoweb")

@task
def e2e(ctx):
    ctx.run("playwright install")
    ctx.run("pytest ilmoweb/tests/playwright/ --headed --base-url http://127.0.0.1:8000/")
