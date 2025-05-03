from framework import runner, task


with runner():

    @task()
    def hello_world():
        print("Hello world")

    @task(required_by=[hello_world])
    def first():
        print("This goes first")
