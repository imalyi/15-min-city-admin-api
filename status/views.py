from rest_framework.response import Response
from rest_framework.decorators import api_view
import json
import status.SUB_TASK_STATUSES as subtask_statuses_list
import status.TASK_STATUSES as task_statuses_list


@api_view()
def subtask_statuses(request):
    task_statuses = [subtask_statuses_list.WAITING, subtask_statuses_list.DONE, subtask_statuses_list.ERROR, subtask_statuses_list.RUNNING,
                     subtask_statuses_list.STOPPED, subtask_statuses_list.CANCELED]
    return Response(json.dumps(task_statuses))

@api_view()
def task_statuses(request):
    task_statuses = [task_statuses_list.WAITING, task_statuses_list.DONE, task_statuses_list.ERROR, task_statuses_list.RUNNING,
                     task_statuses_list.STOPPED, task_statuses_list.CANCELED]
    return Response(json.dumps(task_statuses))