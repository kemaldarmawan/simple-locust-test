import yaml
from locust import HttpLocust, TaskSet

config = yaml.load(file('api.yml'))


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


def load_task():
    tasks = {}
    for request in config['routes']:
        tasks[create_task(request)] = request.get('weight', 1)
    return tasks


class UserBehavior(TaskSet):
    tasks = load_task()


class WebsiteUser(HttpLocust):
    host = config['host']
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
