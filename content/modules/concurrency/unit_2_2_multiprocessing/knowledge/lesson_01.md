# Unit 2.2: Multiprocessing

---

## 1. What

### Simple Definition
Imagine you and your coworkers are all trying to work on different projects in a single, cramped cubicle (Threading). You share the same desk, the same stapler, and the same whiteboard. But whenever someone wants to talk or write on the board, only one person can speak at a time because of a strict company rule (the Global Interpreter Lock / GIL).

Now imagine the company moves each of you into **your own private office in separate buildings** (Multiprocessing). 
- You have your own desk, your own computer, and your own coffee machine (Isolated Memory).
- You can work at 100% full speed on your own projects at the exact same physical second without waiting for anyone else (True Parallelism across CPU cores).
- If you need to send a document to your coworker, you cannot simply point to the desk. You must put the document into an envelope, seal it, and hand it to a postal courier who delivers it to the other building (Inter-Process Communication / Pickling).

In Python, the `multiprocessing` module allows your programs to spawn completely independent operating system processes. Each process runs its own Python interpreter and has its own private memory heap, completely bypassing the GIL to deliver true multi-core parallel execution.

### What Problems Does Multiprocessing Solve?
1. **The Python GIL Barrier on Multi-Core Hardware**: In standard Python, threads cannot run pure Python code on more than one CPU core at the same time. Multiprocessing bypasses this restriction by creating multiple Python processes, allowing you to use 100% of your 8, 16, or 64 CPU cores.
2. **Crash Isolation**: If one worker process encounters a catastrophic memory error (like a segmentation fault in a C-library or an out-of-memory crash), only that single worker dies. The main application and all other worker processes stay alive and healthy.
3. **True Memory Isolation**: Because processes do not share memory address spaces, it is physically impossible for Process A to accidentally overwrite or corrupt a variable inside Process B.

### Key Terms You Must Know
- **Process**: An independent executing program managed by the OS, with its own private memory.
- **IPC (Inter-Process Communication)**: Mechanisms used by isolated processes to send messages back and forth (`multiprocessing.Queue`, `multiprocessing.Pipe`, `SharedMemory`).
- **Pickling / Serialization**: The process of converting Python objects (dictionaries, numbers, lists) into a stream of bytes so they can be transmitted across process boundaries.
- **Spawn vs. Fork**: The method used by the operating system to create child processes. Windows and macOS use `spawn` (which starts a brand-new Python interpreter from scratch), while Linux historically used `fork` (which copies the parent memory space).

---

## 2. Examples

Let us explore 4 complete, runnable examples illustrating process creation, IPC communication, and shared memory.

### Example 1: Creating and Joining an Operating System Process
The simplest way to run code in a separate process using `multiprocessing.Process`.

```python
import multiprocessing
import os
import time

def process_worker(worker_name: str, sleep_duration: float):
    """Function executed in a completely independent OS process."""
    print(f"[{worker_name}] Starting worker in Process PID: {os.getpid()} (Parent PID: {os.getppid()})")
    time.sleep(sleep_duration)
    print(f"[{worker_name}] Finished work cleanly.")

# CRITICAL FOR WINDOWS: Always guard process startup with __name__ == '__main__'!
if __name__ == "__main__":
    print(f"[Main Process] Running in PID: {os.getpid()}")
    
    # Instantiate child process
    child = multiprocessing.Process(
        target=process_worker,
        args=("Worker-Alpha", 0.5),
        name="ChildProcess-1"
    )
    
    child.start()  # OS creates new Python process
    print(f"[Main Process] Child process launched. Waiting for it to finish...")
    child.join()   # Blocks main process until child finishes
    print(f"[Main Process] Child finished with exit code: {child.exitcode}")
```

**Console Output**:
```text
[Main Process] Running in PID: 12450
[Main Process] Child process launched. Waiting for it to finish...
[Worker-Alpha] Starting worker in Process PID: 12451 (Parent PID: 12450)
[Worker-Alpha] Finished work cleanly.
[Main Process] Child finished with exit code: 0
```

---

### Example 2: Inter-Process Communication Using `multiprocessing.Queue`
Because processes do not share variables, passing data back to the main process requires an IPC queue. Python automatically pickles data placed into `multiprocessing.Queue`.

```python
import multiprocessing
import os

def calculate_square_in_process(number: int, result_queue: multiprocessing.Queue):
    """Calculates square and sends result back via IPC queue."""
    res = number * number
    print(f"[Child PID {os.getpid()}] Calculated {number}^2 = {res}")
    result_queue.put((number, res))

if __name__ == "__main__":
    # Create an IPC queue
    ipc_queue = multiprocessing.Queue()
    
    processes = []
    inputs = [10, 20, 30, 40]
    
    # Launch 4 separate child processes
    for num in inputs:
        p = multiprocessing.Process(target=calculate_square_in_process, args=(num, ipc_queue))
        processes.append(p)
        p.start()
        
    for p in processes:
        p.join()
        
    # Drain results from IPC queue
    results = []
    while not ipc_queue.empty():
        results.append(ipc_queue.get())
        
    print(f"[Main Process] Collected all results: {results}")
```

**Console Output**:
```text
[Child PID 18201] Calculated 10^2 = 100
[Child PID 18202] Calculated 20^2 = 400
[Child PID 18203] Calculated 30^2 = 900
[Child PID 18204] Calculated 40^2 = 1600
[Main Process] Collected all results: [(10, 100), (20, 400), (30, 900), (40, 1600)]
```

---

### Example 3: Bidirectional Communication with `multiprocessing.Pipe`
When exactly two processes need a private communication channel, a **Pipe** is faster and lighter than a queue. A pipe gives you two connection endpoints: `conn1` and `conn2`.

```python
import multiprocessing

def patient_monitor_agent(child_conn):
    """Child process that listens for commands from parent."""
    # Wait for instructions from parent process
    command = child_conn.recv()
    print(f"[Child Agent] Received command from parent: '{command}'")
    
    # Process instruction and send back telemetry
    telemetry = {"heart_rate": 75, "oxygen": 99, "status": "NOMINAL"}
    child_conn.send(telemetry)
    child_conn.close()

if __name__ == "__main__":
    # Create bidirectional pipe
    parent_conn, child_conn = multiprocessing.Pipe()
    
    p = multiprocessing.Process(target=patient_monitor_agent, args=(child_conn,))
    p.start()
    
    # Send message to child
    print("[Parent] Sending 'QUERY_VITALS' command to child agent...")
    parent_conn.send("QUERY_VITALS")
    
    # Receive response from child
    response = parent_conn.recv()
    print(f"[Parent] Received response from child: {response}")
    
    p.join()
    parent_conn.close()
```

**Console Output**:
```text
[Parent] Sending 'QUERY_VITALS' command to child agent...
[Child Agent] Received command from parent: 'QUERY_VITALS'
[Parent] Received response from child: {'heart_rate': 75, 'oxygen': 99, 'status': 'NOMINAL'}
```

---

### Example 4: Zero-Copy Shared Memory for Large Arrays (`multiprocessing.shared_memory`)
Pickling a 500-megabyte array across an IPC pipe takes several seconds. Python 3.8+ introduced `multiprocessing.shared_memory`, which allows processes to map the exact same physical RAM block into their address spaces for zero-copy multi-core sharing!

```python
import multiprocessing
from multiprocessing import shared_memory
import numpy as np

def modify_shared_array(shm_name: str, shape: tuple, dtype: str):
    """Child process attaches to the shared memory block directly."""
    existing_shm = shared_memory.SharedMemory(name=shm_name)
    # Create numpy array backed by the shared memory buffer
    shared_array = np.ndarray(shape, dtype=dtype, buffer=existing_shm.buf)
    
    print(f"[Child Process] Doubling all elements in shared memory array...")
    shared_array[:] = shared_array * 2
    existing_shm.close()

if __name__ == "__main__":
    # Create initial numpy array in main process
    original_data = np.array([10, 20, 30, 40, 50], dtype=np.int64)
    print(f"[Main Process] Original data: {original_data}")
    
    # Allocate shared memory block
    shm = shared_memory.SharedMemory(create=True, size=original_data.nbytes)
    # Map array into shared buffer
    shm_array = np.ndarray(original_data.shape, dtype=original_data.dtype, buffer=shm.buf)
    shm_array[:] = original_data[:]
    
    # Launch child process and pass ONLY the name of the memory block
    p = multiprocessing.Process(
        target=modify_shared_array,
        args=(shm.name, original_data.shape, str(original_data.dtype))
    )
    p.start()
    p.join()
    
    print(f"[Main Process] Array after child execution: {shm_array}")
    
    # Always clean up shared memory!
    shm.close()
    shm.unlink()
```

**Console Output**:
```text
[Main Process] Original data: [10 20 30 40 50]
[Child Process] Doubling all elements in shared memory array...
[Main Process] Array after child execution: [ 20  40  60  80 100]
```

---

## 3. Explanation

### Process Memory Isolation Visualized

```text
       OPERATING SYSTEM PHYSICAL HARDWARE (16 CPU CORES / 32 GB RAM)
┌──────────────────────────────────────────────────────────────────┐
│                                                                  │
│  [PROCESS 1: Main (PID 101)]         [PROCESS 2: Child (PID 102)]│
│  ┌─────────────────────────┐         ┌─────────────────────────┐ │
│  │ Python Interpreter (GIL)│         │ Python Interpreter (GIL)│ │
│  │ Private Heap Memory     │         │ Private Heap Memory     │ │
│  │ Global Variables:       │         │ Global Variables:       │ │
│  │   counter = 100         │         │   counter = 0 (ISOLATED)│ │
│  └────────────┬────────────┘         └────────────▲────────────┘ │
│               │                                   │              │
│               │     Inter-Process Communication   │              │
│               └────► [IPC Pipe / Queue] ──────────┘              │
│                      (Pickled Byte Stream)                       │
│                                                                  │
│                 [SHARED MEMORY BLOCK (Optional)]                 │
│                 (Direct Zero-Copy RAM Mapping)                   │
└──────────────────────────────────────────────────────────────────┘
```

Notice that both processes have their own private GIL! Because each process has its own GIL, **they run in true hardware parallel on separate CPU cores**.

---

### Step-by-Step Breakdown: What Happens During `process.start()`?

1. **Operating System Call**: The main process requests the OS kernel to create a child process.
   - On **Linux** (`fork`): The OS clones the entire parent process address space (using Copy-on-Write).
   - On **Windows and macOS** (`spawn`): The OS creates a fresh executable, launches a brand new `python.exe` process, and re-imports the main script.
2. **Serialization (Pickling)**: Python takes the target function and all arguments in `args`, serializes them into bytes using `pickle`, and writes them across an operating system pipe to the child.
3. **Child Execution**: The child process unpacks the arguments and begins executing the target function on its own dedicated CPU core.
4. **Process Exit**: When the function returns, the child process exits with an exit code (0 for success, non-zero for error). The parent process reads this exit code when calling `join()`.

---

### IPC Options Compared

| Mechanism | Speed | Communication Style | Maximum Endpoints | Best Use Case |
| :--- | :--- | :--- | :--- | :--- |
| **`multiprocessing.Queue`** | Moderate (Pickling) | Thread-safe & Process-safe FIFO | Many producers, many consumers | Distributing tasks to multiple workers |
| **`multiprocessing.Pipe`** | Fast (Pickling) | Direct point-to-point channel | Exactly 2 processes (1 on each end) | 1-to-1 coordinator-to-worker commands |
| **`SharedMemory`** | Ultra-Fast (Zero-Copy) | Direct shared RAM buffer | Multiple processes reading/writing | Large NumPy arrays, computer vision images |
| **`Manager`** | Slowest (RPC Proxy) | Networked proxy server for dicts/lists | Many processes | Sharing complex dynamic objects safely |

---

## 4. Why Multiprocessing Matters

### 1. 100% Utilization of Multi-Core Processors
If you buy an AMD Ryzen 16-core processor or deploy an Amazon Web Services 64-core c6i instance, running standard Python threads will only use **one single core**. Multiprocessing is the primary standard-library tool that allows Python applications to scale linearly across all CPU cores.

### 2. Immunity to Memory Leaks in Third-Party Libraries
C-extensions (like image decoders or machine learning packages) can sometimes leak memory. By executing tasks in child processes and terminating the processes when done, the operating system kernel instantly reclaims 100% of the allocated memory, eliminating memory leaks permanently.

### 3. Fault Isolation
If a worker thread encounters a fatal segmentation fault, it immediately crashes your entire server. If a child process crashes, the parent catches the non-zero exit code, logs the error, and simply spawns a replacement worker without dropping service for other users.

---

## 5. Advantages & Disadvantages

### Advantages
- **True Multi-Core Parallelism**: Unconstrained by the GIL for CPU-bound computations.
- **Robust Process Isolation**: Memory corruption in one process cannot affect another.
- **Full Support for Native C Extensions**: Safely isolates unstable native code.

### Disadvantages
- **High Memory Footprint**: Each Python process consumes 20–50 MB of base RAM.
- **IPC Serialization Overhead**: Sending large Python objects across queues is slow due to `pickle`.
- **Startup Latency**: Spawning a new OS process takes 20–100 milliseconds, compared to less than 1 millisecond for a thread.

---

## 6. Real-World Use Cases

### Domain 1: Healthcare (High-Throughput Genomic Sequencing)
- **Problem**: Next-generation genomic sequencers output millions of 100-base-pair DNA reads that must be searched for genetic markers. A single thread takes 4 hours to align a patient's genome.
- **Solution**: A multiprocessing pipeline splits the raw FASTQ file into chunks and processes them across 32 child processes.
- **Benefits**: Processing time drops from 4 hours down to 8.5 minutes.

### Domain 2: eCommerce (Product Catalog Image Optimization)
- **Problem**: An online retail platform receives 50,000 product photos from suppliers daily. Each image must be resized, compressed to WebP, and watermarked. Doing this sequentially takes all night.
- **Solution**: A pool of child processes drains an image processing queue, utilizing all server cores.
- **Benefits**: All 50,000 photos are processed, optimized, and uploaded to the CDN in 25 minutes.

### Domain 3: Banking (Monte Carlo Portfolio Risk Modeling)
- **Problem**: Investment banks calculate Value at Risk (VaR) by simulating 1,000,000 market fluctuation scenarios before market open.
- **Solution**: Each child process runs 100,000 independent simulation paths using NumPy and writes summarized risk metrics to an IPC queue.
- **Benefits**: Risk reports complete before market opening bell, meeting regulatory compliance requirements.

---

## 7. Best Practices

### Practice 1: Always Guard Code with `if __name__ == '__main__':`
**When to apply**: Mandatory on Windows and macOS.
**Why**: Without this guard, spawned child processes will re-execute the module from top to bottom, creating an infinite recursive loop of child processes that crashes your operating system.

---

### Practice 2: Only Pass Picklable Objects Through IPC
**When to apply**: When passing arguments or queue items.
**Why**: File handles, open database sockets, and lambda functions cannot be pickled. Passing them causes `PicklingError`.

---

### Practice 3: Always Call `join()` on Finished Processes
**When to apply**: After starting child processes.
**Why**: If a parent process does not call `join()`, terminated child processes remain in the operating system process table as **zombie processes**, leaking process IDs.

---

## 8. Top 3 Mistakes & Anti-Patterns

### Mistake 1: Missing the `if __name__ == '__main__':` Guard
#### What's the Problem?
Writing multiprocessing code at the top level of a script without the `__name__ == '__main__':` guard.
#### Why It Happens
It works on Linux (due to `fork`), so developers assume it works everywhere.
#### Impact
On Windows and macOS, the script crashes immediately with `RuntimeError: An attempt has been made to start a new process before the current process has finished its bootstrapping phase`.
#### Correct Approach
Always wrap all process creation code inside `if __name__ == '__main__':`.

---

### Mistake 2: Passing Huge Objects Across IPC Queues
#### What's the Problem?
Putting a 2-gigabyte list of objects into a `multiprocessing.Queue`.
#### Why It Happens
Developers treat `multiprocessing.Queue` like a regular Python list.
#### Impact
The main process freezes for several seconds serializing the list, memory usage doubles, and queue buffers can deadlock.
#### Correct Approach
Write large datasets to disk or use `multiprocessing.shared_memory`.

---

### Mistake 3: Forgetting to Clean Up Shared Memory
#### What's the Problem?
Creating a `shared_memory.SharedMemory` block and not calling `.unlink()`.
#### Why It Happens
Assuming Python garbage collection will automatically delete OS-level shared memory.
#### Impact
The shared memory block persists in the operating system RAM even after Python exits, permanently leaking system RAM until the computer is rebooted.
#### Correct Approach
Always use a `try...finally` block:
```python
shm = shared_memory.SharedMemory(create=True, size=1024)
try:
    # Use memory
    pass
finally:
    shm.close()
    shm.unlink()  # Permanently destroys the OS shared memory block
```
