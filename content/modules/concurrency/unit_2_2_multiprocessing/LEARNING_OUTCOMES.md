# Unit 2.2: Multiprocessing - Learning Outcomes

## Overview
Because CPython's Global Interpreter Lock restricts thread execution to one CPU core, achieving true hardware parallelism for compute-intensive tasks requires spawning separate operating system processes. Each process hosts its own private Python interpreter instance, memory space, and GIL. This unit covers creating and managing processes via `multiprocessing.Process`, process synchronization, inter-process communication using `multiprocessing.Queue` and `multiprocessing.Pipe`, and cross-process serialization rules.

**Estimated Time**: 5-7 hours
- Knowledge: 90 min
- Exercises: 90-120 min
- App Labs: 2-3 hours

---

## Learning Outcomes

After completing this unit, you will be able to:

### Process Architecture & Lifecycle
- [ ] **Instantiate** and run worker processes using `multiprocessing.Process(target=..., args=...)`.
- [ ] **Contrast** memory isolation in processes (separate heaps, zero shared state by default) with shared memory in threads.
- [ ] **Manage** process lifecycles using `.start()`, `.join()`, `.is_alive()`, and `.terminate()`.
- [ ] **Implement** the `if __name__ == '__main__':` entry point guard required for Windows process spawning (`spawn` start method).

### Inter-Process Communication (IPC)
- [ ] **Transmit** pickled data safely between processes using `multiprocessing.Queue`.
- [ ] **Establish** two-way point-to-point communication channels using `multiprocessing.Pipe()`.
- [ ] **Explain** serialization requirements (pickleability) for all arguments passed across process boundaries.

### Real-World Engineering Application (Healthcare)
- [ ] **Construct** a multi-core genomic sequence alignment worker pool that partitions multi-megabyte DNA FASTA files across physical CPU cores for parallel pattern matching.
