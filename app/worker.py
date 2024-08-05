import threading
import queue
import time
import pendulum

import uuid

from client import run_benchmark
from data.datastore import Storage
from data.models import Report, User

class Worker(threading.Thread):
    def __init__(self, storage: Storage, *args, **kwargs):
        self.storage = storage
        self.q = queue.Queue()
        super(Worker, self).__init__(*args, **kwargs)

    def put(self, user: User, benchmark_type: str):
        task_id = str(uuid.uuid4())
        new_report = Report(task_id, "queued", pendulum.now().to_iso8601_string(), '', user.id)
        self.storage.insert(new_report)
        self.q.put((task_id, benchmark_type))
        return {"task_id": task_id}

    def run(self):
        while True:
            id, item = self.q.get()
            if (item == "quit"):
                return
            # report = Storage
            self.task_states[id] = "progress"
            print(f'Working on {id} - {item}')
            run_benchmark(id, 'aws_compliance.benchmark.cis_v300')
            print(f'Finished {item}')
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