import yaml
from locust import HttpLocust, TaskSet, task

config = yaml.load(file('locust.yml'))


def create_task(request):
    def task(l):
        method = request.get('method', 'GET')
        url = request['url']
        name = request.get('name', None)
        body = request.get('data', None)
        params = request.get('params', None)
        headers = request.get('headers', None)
        l.client.request(name=name,
                         method=method,
                         url=url,
                         params=params,
                         data=body,
                         headers=headers)
    return task


def create_task_class(task_config):
    class TaskSetClass(TaskSet):
        def on_start(self):
            if 'on_start' in task_config:
                for request in task_config['on_start']['routes']:
                    create_task(request)(self)
            pass
        tasks = load_task(task_config)

        @task
        def stop(self):
            self.interrupt()

    return TaskSetClass


def load_task_class(tasks_config):
    tasks = {}
    for task_set in tasks_config:
        tasks[create_task_class(task_set)] = task_set.get('weight', 1)
    return tasks


def load_task_method(routes):
    tasks = {}
    for request in routes:
        tasks[create_task(request)] = request.get('weight', 1)
    return tasks


def load_task(config):
    tasks = {}
    if 'task' in config:
        tasks[create_task_class(config['task'])] = 1
    if 'tasks' in config:
        tasks.update(load_task_class(config['tasks']))
    if 'routes' in config:
        tasks.update(load_task_method(config['routes']))
    return tasks


class UserBehavior(TaskSet):
    tasks = load_task(config)

    def on_start(self):
        if 'on_start' in config:
            for request in config['on_start']['routes']:
                create_task(request)(self)


class WebsiteUser(HttpLocust):
    host = config['host']
    task_set = UserBehavior
    min_wait = config.get('min_wait', 1000)
    max_wait = config.get('max_wait', 1000)
