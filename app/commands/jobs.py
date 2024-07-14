
def job__run(ctx, name):
    """Run a job by name."""
    if not name:
        raise ValueError("Job name cannot be empty")

    job_module = __import__(f'app.jobs.{name}', fromlist=['run'])

    if hasattr(job_module, 'run') and callable(job_module.run):
        job_module.run(ctx)
    else:
        raise ValueError(f"Job '{name}' does not have a 'run' function")
job__run.args = [("name", {"type": str, "help": "Job name"})]
