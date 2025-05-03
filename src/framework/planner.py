from framework.task import Task


def planner(tasks: list[Task]):
    result: list[Task] = []
    dependencies: dict[Task, list[Task]] = {}

    for task in tasks:
        dependencies[task] = []

    for task in tasks:
        for subtask in task.requires:
            dependencies[task].append(subtask)
        for subtask in task.required_by:
            dependencies[subtask].append(task)

    while True:
        if not dependencies:
            break

        tasks_to_pop = []

        for task in dependencies:
            if not dependencies[task]:
                result.append(task)
                tasks_to_pop.append(task)

                for t in dependencies:
                    if task in dependencies[t]:
                        dependencies[t].remove(task)

        for task in tasks_to_pop:
            dependencies.pop(task)

    return result
