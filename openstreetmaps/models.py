from django.db import models


class OSMTask(models.Model):
    region = models.CharField(max_length=250)

    @property
    def status(self):
        running_results = OSMTaskResult.objects.filter(finish_date=None, task=self)
        if running_results.exists():
            return "RUNNING"
        latest_result = OSMTaskResult.objects.filter(task=self).order_by('-finish_date').first()
        if latest_result and latest_result.errors == 0:
            return "DONE"
        elif latest_result and latest_result.errors > 0:
            return "DONE_WITH_ERRORS"
        else:
            return "NEVER RUN"


class OSMTaskResult(models.Model):
    task = models.ForeignKey(OSMTask, on_delete=models.CASCADE)
    start_date = models.DateTimeField(auto_now=True)
    finish_date = models.DateTimeField(null=True, blank=True, default=None, unique=True)
    items_collected = models.IntegerField(default=0)

    @property
    def errors(self):
        return OSMError.objects.filter(task_result=self).count()

    def update_progress(self, progress: int):
        self.items_collected += progress
        self.save()

    def add_error(self, data: str, type: str) -> None:
        OSMError.objects.create(task_result=self, data=data, type=type)


class OSMError(models.Model):
    task_result = models.ForeignKey(OSMTaskResult, on_delete=models.CASCADE)
    data = models.CharField(max_length=800)
    date = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=260)
