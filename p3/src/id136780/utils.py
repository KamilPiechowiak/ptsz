def compute_loss(order, tasks, m):
    t = [0 for _ in range(m)]
    loss = 0
    for idx in order:
        task = tasks[idx-1]
        prev_time = 0
        for i in range(m):
            t[i] = max(t[i], prev_time)+task.duration[i]
            prev_time = t[i]
        if task.due_date < prev_time:
            loss+=task.weight*(prev_time-task.due_date)
    return loss/sum([task.weight for task in tasks])
           