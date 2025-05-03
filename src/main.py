from framework import runner, shell, task


with runner():

    @task()
    def hello_world():
        shell("echo 'Hello world!'")

    @task(required_by=[hello_world])
    def first():
        print("This goes first")
