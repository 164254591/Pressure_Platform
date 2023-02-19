import os
from django_task_mq import mq_init
mq_init(os.path.dirname(os.path.abspath(__file__)))