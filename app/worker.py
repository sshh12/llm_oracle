from multiprocessing import Process

from server.predict_job import main

JOBS = 5

if __name__ == "__main__":
    procs = []
    for _ in range(JOBS):
        p = Process(target=main)
        p.start()
        procs.append(p)
    [p.join() for p in procs]
