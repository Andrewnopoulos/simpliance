import threading
import queue
import time
import pendulum

import uuid

from client import run_benchmark, validate_input
from data.datastore import Storage
from data.models import Report, User, AuthKeys

import threading

class Worker2:
    _instance = None
    _lock = threading.Lock()

    db_path = None

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(Worker2, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._thread = threading.Thread(target=self._run)
            self._thread.daemon = True
            self._initialized = True
            self.q = queue.Queue()

    def start_thread(self):
        self._thread.start()
    
    def stop_thread(self):
        self.q.put('quit')
        self._thread.join()

    def put(self, user: User, keys: AuthKeys, benchmark_type: str):
        try:
            validate_input(benchmark_type)
        except ValueError as e:
            print(f"Input validation failed: {e}")
            return str(e)
        report_id = str(uuid.uuid4())
        new_report = Report(
            report_id,
            "queued",
            pendulum.now().to_iso8601_string(),
            '',
            benchmark_type,
            user.id,
            keys.id
        )
        with Storage(self.db_path) as s:
            s.insert(new_report)
        self.q.put(report_id)
        return {"report_id": report_id}

    def _run(self):
        while True:
            print("inside running thread")
            report_id = self.q.get()
            if (report_id == "quit"):
                return
            with Storage(self.db_path) as s:
                report = s.get_one(Report, {'id': report_id})
                if not report:
                    print(f"error fetching report with id {report_id}")
                    s.delete(report)
                    self.q.task_done()
                    time.sleep(1)
                    continue

                report.process_state = "progress"
                
                s.update(report)
                print(f'Working on {report_id}')
                print(f'benchmark: {report.benchmark}')
                print(f'auth keys: {report.auth_key_id}')
                # run_benchmark(id, 'aws_compliance.benchmark.cis_v300') # NOT USED
                run_benchmark(report)
                print(f'Finished {report.benchmark}')
                self.q.task_done()
                report.process_state = "done"
                report.datetime_completed = pendulum.now().to_iso8601_string()
                rows = s.update(report)
                print(f"updated report: {rows}")
            time.sleep(1)

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
    
    def exit(self):
        self.q.put((None, 'quit'))

    def run(self):
        while True:
            id, item = self.q.get()
            if (item == "quit"):
                return
            report = self.storage.get_one(Report, {'id': id})
            if not report:
                print(f"error fetching report with id {id}")
                self.storage.delete(report)
                self.q.task_done()
                time.sleep(1)
                continue

            report.process_state = "progress"
            self.storage.update(report)
            print(f'Working on {id} - {item}')
            # run_benchmark(id, 'aws_compliance.benchmark.cis_v300')
            run_benchmark(id, item)
            print(f'Finished {item}')
            self.q.task_done()
            report.process_state = "done"
            report.datetime_completed = pendulum.now().to_iso8601_string()
            self.storage.update(report)
            time.sleep(1)


if __name__ == "__main__":
    worker = Worker()
    worker.daemon = True

    worker.start()
    worker.put('hello')
    worker.put('there')
    worker.put("quit")
    worker.join()