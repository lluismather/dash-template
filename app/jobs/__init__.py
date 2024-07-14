import os
from invoke import Collection

ns = Collection()
jobs_dir = os.path.dirname(__file__)

for file in os.listdir(os.path.dirname(__file__)):
    if file.endswith('.py') and file != '__init__.py':
        module_name = file[:-3]
        module = __import__(f'app.jobs.{module_name}', fromlist=['run'])
        if hasattr(module, 'run'):
            ns.add_task(module.run, name=module_name)

