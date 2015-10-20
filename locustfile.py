import yaml
from locust import HttpLocust, TaskSet

config = yaml.load(file('api.yaml'))


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
    def on_start(self):
        if 'on_start' in config:
            for request in config['on_start']:
                print 'hello'
                start_task = create_task(request)
                print type(start_task)
                start_task(self)
    tasks = load_task()


class WebsiteUser(HttpLocust):
    host = config['host']
    task_set = UserBehavior
    min_wait = 5000
    max_wait = 9000
