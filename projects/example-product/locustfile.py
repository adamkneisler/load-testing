from locust import HttpLocust, TaskSet, task

import utils
import resource

resource.setrlimit(resource.RLIMIT_NOFILE, (999999, 999999))

from web import IFrame
from api import API


class MSL_Load(HttpLocust):
    task_set = API
    min_wait = 5000
    max_wait = 9000

class IFrame_Load(HttpLocust):
    task_set = IFrame
    min_wait = 5000
    max_wait = 9000