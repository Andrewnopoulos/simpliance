import threading
import queue
import time

import uuid

from client import run_benchmark

class Worker(threading.Thread):
    def __init__(self, task_states: dict, *args, **kwargs):
        self.task_states = task_states
        self.q = queue.Queue()
        super(Worker, self).__init__(*args, **kwargs)

    def put(self, item):
        task_id = str(uuid.uuid4())
        self.task_states[task_id] = "queued"
        self.q.put((task_id, item))
        return {"task_id": task_id}

    def run(self):
        while True:
            id, item = self.q.get()
            if (item == "quit"):
                return
            self.task_states[id] = "progress"
            print(f'Working on {id} - {item}')
            print(f'Finished {item}')
            run_benchmark(id, 'aws_compliance.benchmark.cis_v300')
            self.q.task_done()
            self.task_states[id] = "done"
            time.sleep(1)


if __name__ == "__main__":
    worker = Worker()
    worker.daemon = True

    worker.start()
    worker.put('hello')
    worker.put('there')
    worker.put("quit")
    worker.join()