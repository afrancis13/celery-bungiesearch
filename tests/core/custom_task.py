from celery import Task


class CustomTask(Task):
    ignore_result = True

    def apply_async(self, *args, **kwargs):
        super(CustomTask, self).apply_async(*args, **kwargs)
