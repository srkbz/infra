from framework import runner, task, shell


with runner():

    @task()
    def hello_world():
        shell("echo 'Hello world!'")

    @task(required_by=[hello_world])
    def first():
        print("This goes first")

    @task(requires=[hello_world])
    def last():
        print("Bye!")
