# Multiprocessing-work-OS5

This script clearly shows the work with the processes of the multiprocessing module.
### Description of work
There are 3 possible states of threads (processes):
1. Pool (Пул)
2. Work (Работают)
3. Expectation (В ожидании)

The threads in the pool have been created but are waiting to run.

Running threads are loaded, when the task is completed up to 100%, they return to the pool with 0% progress.

The waiting threads are killed but keep their execution progress.
