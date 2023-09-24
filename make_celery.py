from celery import Celery


def make_celery(app):
    celery = Celery(
        app.import_name,
        broker='redis://localhost',
        backend='redis://localhost'
    )

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery
