# Unit 2.4: Asynchronous Programming

---

## 1. What

### Simple Definition
Imagine you walk into a coffee shop. 
- In a **synchronous** coffee shop, the barista takes your order for a latte, walks over to the espresso machine, waits 3 minutes while the milk steams and coffee brews, hands you your cup, and only *then* calls the next person in line. If 20 people are waiting, the 20th person waits an entire hour!
- In a **multi-threaded** coffee shop, the owner hires 20 baristas so each customer has their own dedicated server. But having 20 baristas standing behind a small counter causes everyone to bump into each other, and paying 20 salaries is extremely expensive (threads consume lots of memory).
- In an **asynchronous (Asyncio)** coffee shop, there is only **one** barista. The barista takes your order, starts the espresso machine, and while the machine is running (waiting for hot water and steam), the barista *immediately* turns to the next customer, takes their order, and starts their muffin in the toaster. As soon as the espresso machine dings, the barista pours the milk and hands you your latte. 

One barista handles 100 customers smoothly because they **never stand around doing nothing while waiting for machines to finish**.

In Python, **Asynchronous Programming** (`asyncio`) is this exact model. Instead of having the operating system pause and switch between hundreds of heavy threads, a single Python process runs an **Event Loop**. Whenever a task has to wait for network data, a database response, or a file read, it voluntarily yields control back to the event loop so other tasks can run in the meantime.

### What Problems Does It Solve?
1. **The 10,000 Concurrent Connections Problem (C10k)**: Traditional operating systems struggle to run more than 1,000 threads simultaneously because each thread reserves several megabytes of stack memory. Asyncio coroutines take only a few kilobytes of RAM each, allowing a single server to maintain 50,000+ simultaneous connections (e.g., chat applications, IoT sensors, live sports feeds).
2. **Elimination of Lock Bugs**: Because your code runs on a single thread, you do not have two threads writing to the same memory address at the same physical microsecond. Code only switches between tasks at explicit `await` statements that you write yourself!
3. **Massive Throughput on Network Calls**: Web scraping, microservice querying, and third-party API integration become dozens of times faster without burning CPU cores.

### Key Terms You Must Know
- **Coroutine**: A special Python function defined with `async def`. It can be paused and resumed.
- **`await`**: The keyword placed before a slow operation. It tells Python: *"Pause this function here while waiting, and let other tasks run on the event loop."*
- **Event Loop**: The central traffic controller in Python that keeps track of all active coroutines and decides which one runs next.
- **Task**: A coroutine that has been scheduled to run in the background on the event loop (`asyncio.create_task()`).
- **`asyncio.gather()`**: A function that launches multiple coroutines simultaneously and waits for all of them to finish.

---

## 2. Examples

Let us walk through 4 complete, runnable examples from basic syntax to advanced enterprise patterns.

### Example 1: Your First Coroutine (`async def` and `await`)
Notice the syntax: we define the function using `async def`, wait non-blockingly using `await asyncio.sleep()`, and start the engine using `asyncio.run()`.

```python
import asyncio
import time

async def brew_coffee(customer_name: str, seconds_to_brew: float) -> str:
    print(f"[Coffee Station] Starting to brew coffee for {customer_name}...")
    # asyncio.sleep simulates waiting for a network request or database read.
    # CRITICAL: This yields control back to the event loop; it does NOT freeze the computer!
    await asyncio.sleep(seconds_to_brew)
    print(f"[Coffee Station] Ding! Coffee for {customer_name} is ready!")
    return f"Hot Latte for {customer_name}"

async def main():
    start_time = time.perf_counter()
    
    # We await the coroutine to get its return value
    cup = await brew_coffee("Alice", 1.0)
    print(f"Customer received: {cup}")
    
    elapsed = time.perf_counter() - start_time
    print(f"Total time taken: {elapsed:.2f} seconds")

# asyncio.run creates the event loop, runs main(), and closes the loop cleanly
if __name__ == "__main__":
    asyncio.run(main())
```

**Console Output**:
```text
[Coffee Station] Starting to brew coffee for Alice...
[Coffee Station] Ding! Coffee for Alice is ready!
Customer received: Hot Latte for Alice
Total time taken: 1.01 seconds
```

---

### Example 2: Concurrent Execution with `asyncio.gather()`
If we brew coffee for Alice (1 sec), Bob (1 sec), and Charlie (1 sec) sequentially, it takes 3 seconds. With `asyncio.gather()`, all three brew simultaneously, taking only 1 second in total!

```python
import asyncio
import time

async def fetch_webpage(url: str, delay: float) -> str:
    print(f"--> [Network] Request sent to {url}")
    await asyncio.sleep(delay)  # Simulated download latency
    print(f"<-- [Network] Data received from {url}")
    return f"200 OK from {url}"

async def main():
    t0 = time.perf_counter()
    
    # Schedule all 3 network requests concurrently!
    results = await asyncio.gather(
        fetch_webpage("https://api.github.com", 0.5),
        fetch_webpage("https://api.slack.com", 0.3),
        fetch_webpage("https://api.stripe.com", 0.4)
    )
    
    elapsed = time.perf_counter() - t0
    print(f"\nAll requests completed in {elapsed:.2f} seconds!")
    for res in results:
        print(f"  Result: {res}")

if __name__ == "__main__":
    asyncio.run(main())
```

**Console Output**:
```text
--> [Network] Request sent to https://api.github.com
--> [Network] Request sent to https://api.slack.com
--> [Network] Request sent to https://api.stripe.com
<-- [Network] Data received from https://api.slack.com
<-- [Network] Data received from https://api.stripe.com
<-- [Network] Data received from https://api.github.com

All requests completed in 0.51 seconds!
  Result: 200 OK from https://api.github.com
  Result: 200 OK from https://api.slack.com
  Result: 200 OK from https://api.stripe.com
```

---

### Example 3: Background Tasks with `asyncio.create_task()`
Sometimes you want to start a long-running background task (like logging an audit event or streaming metrics) and immediately continue running other code without waiting for it to finish.

```python
import asyncio
import time

async def background_telemetry_uploader():
    """Runs continuously in the background."""
    for packet_id in range(1, 4):
        await asyncio.sleep(0.1)
        print(f"  [Background Heartbeat] Telemetry packet #{packet_id} uploaded.")

async def user_request_handler():
    print("[Main App] Handling incoming user login...")
    await asyncio.sleep(0.05)
    print("[Main App] User login verified and session generated!")
    return "User Session Active"

async def main():
    # 1. Fire-and-forget: Schedule background task immediately on the loop
    telemetry_task = asyncio.create_task(background_telemetry_uploader())
    
    # 2. Main workflow runs without being blocked by telemetry
    session = await user_request_handler()
    print(f"[Main App] Returning response to user: {session}")
    
    # 3. Wait for background task to complete before shutting down the script
    await telemetry_task
    print("[Main App] Shutdown complete.")

if __name__ == "__main__":
    asyncio.run(main())
```

**Console Output**:
```text
[Main App] Handling incoming user login...
[Main App] User login verified and session generated!
[Main App] Returning response to user: User Session Active
  [Background Heartbeat] Telemetry packet #1 uploaded.
  [Background Heartbeat] Telemetry packet #2 uploaded.
  [Background Heartbeat] Telemetry packet #3 uploaded.
[Main App] Shutdown complete.
```

---

### Example 4: Enforcing Timeouts and Handling Slow Endpoints (`asyncio.wait_for`)
In real systems, third-party services sometimes hang or disconnect. If you do not set a timeout, your coroutine will wait forever. With `asyncio.wait_for()`, you guarantee your application remains responsive.

```python
import asyncio

async def query_external_hospital_db(patient_id: str, delay: float) -> dict:
    print(f"[Hospital Client] Querying remote record for {patient_id}...")
    await asyncio.sleep(delay)
    return {"patient_id": patient_id, "status": "Active"}

async def safe_query(patient_id: str, delay: float, timeout_limit: float):
    try:
        # Wrap the coroutine with a strict timeout limit
        record = await asyncio.wait_for(
            query_external_hospital_db(patient_id, delay),
            timeout=timeout_limit
        )
        print(f"SUCCESS: Retrieved {record}")
    except asyncio.TimeoutError:
        print(f"WARNING: Database query for {patient_id} exceeded {timeout_limit}s limit! Falling back to cache.")

async def main():
    # Fast query (0.1s delay, 0.5s limit) -> Succeeds
    await safe_query("PAT-100", delay=0.1, timeout_limit=0.5)
    
    # Stalled query (0.8s delay, 0.3s limit) -> Times out safely
    await safe_query("PAT-999", delay=0.8, timeout_limit=0.3)

if __name__ == "__main__":
    asyncio.run(main())
```

**Console Output**:
```text
[Hospital Client] Querying remote record for PAT-100...
SUCCESS: Retrieved {'patient_id': 'PAT-100', 'status': 'Active'}
[Hospital Client] Querying remote record for PAT-999...
WARNING: Database query for PAT-999 exceeded 0.3s limit! Falling back to cache.
```

---

## 3. Explanation

### How the Event Loop Works Under the Hood
At its heart, the Asyncio event loop is essentially a while-loop managed by the operating system's fastest notification system (`epoll` on Linux, `kqueue` on macOS, and `IOCP` on Windows).

```text
                  THE ASYNCIO EVENT LOOP LIFECYCLE
                  
         +-------------------------------------------------+
         |                 EVENT LOOP                      |
         |                                                 |
         |   1. Pick the next READY task from queue        |
         |      (e.g., Task A)                             |
         +-------------------------------------------------+
                                  |
                                  v
                      +-----------------------+
                      | Task A runs Python    |
                      | instructions until it |
                      | hits: "await sock..." |
                      +-----------------------+
                                  |
               +------------------+------------------+
               |                                     |
               v                                     v
       [Yields Control]                       [Registers Socket]
  Task A pauses execution.            OS kernel watches network socket.
  Event loop immediately picks        When data arrives over wire,
  Task B and runs it!                 OS flags Task A as READY again!
```

### Preemptive vs. Cooperative Multitasking: The Key Difference

| Feature | Preemptive Multitasking (Threads) | Cooperative Multitasking (Asyncio) |
| :--- | :--- | :--- |
| **Who controls context switches?** | The Operating System kernel | The Python programmer via `await` |
| **When can a switch happen?** | At **any** millisecond, right in the middle of a line of code! | **Only** when code explicitly says `await` |
| **Are locks required for basic variables?** | **YES**! Unsynchronized writes cause memory corruption | **NO**! Single thread means no simultaneous writes |
| **Memory per task** | ~8 Megabytes per OS thread | ~2 Kilobytes per coroutine |
| **Maximum capacity on 1 server** | ~1,000 to 2,000 threads | 50,000+ simultaneous connections |
| **Effect of a CPU-heavy loop** | OS continues running other threads via time slicing | **FREEZES** the entire program for all users! |

---

## 4. Why Use Asyncio?

### 1. Handling Extreme Concurrency on Modest Hardware
If your company runs a chat system or real-time IoT monitoring service with 20,000 connected devices, running 20,000 operating system threads would require at least 40 to 100 Gigabytes of RAM just for thread stacks. In Asyncio, 20,000 idle socket connections take less than 100 Megabytes of RAM.

### 2. Predictable, Deterministic Code
Because context switches only occur at `await` points, you can read code and know exactly where another task could run. There are no sudden surprises where a thread is interrupted between checking a dictionary key and reading its value.

### 3. Native Integration with Modern Web Frameworks
The most popular high-performance Python web frameworks—such as **FastAPI**, **Starlette**, and **Tornado**—are built natively on top of Asyncio. Writing asynchronous Python allows you to build modern REST APIs that handle thousands of requests per second.

---

## 5. Advantages & Disadvantages

### Advantages
1. **Ultra-Low Memory Footprint**: Thousands of coroutines fit in a few megabytes of memory.
2. **Superior I/O Performance**: Saturates 10-Gigabit network cards with minimal CPU context-switch waste.
3. **No Thread Race Conditions**: Variables cannot be modified by another thread while your function is between two non-await lines.

### Disadvantages
1. **The "What Color is Your Function?" Problem**: You cannot call an `async def` function directly from standard synchronous code without using an event loop runner. Once you introduce async, it tends to spread throughout your codebase.
2. **CPU-Bound Sensitivity**: Any function that performs heavy CPU math without an `await` will block the entire server.
3. **Incompatibility with Blocking Libraries**: Standard libraries like `requests`, `time.sleep()`, and traditional SQL drivers freeze the loop. You must use async equivalents like `httpx` and `asyncpg`.

---

## 6. Real-World Use Cases

### Domain 1: Healthcare (ICU High-Density Telemetry Hub)
- **Problem**: A hospital intensive care unit monitors 100 patients. Each bedside monitor streams ECG, heart rate, and blood oxygen readings over WebSockets every 100 milliseconds. A multi-threaded server drops connections during shift changes when all monitors sync history.
- **Solution**: An **Asyncio WebSocket server**. The single thread handles all 100 incoming streams effortlessly, aggregating vital signs and alerting nursing stations within 5 milliseconds of an arrhythmia event.

### Domain 2: eCommerce (Live Auction Bidding Service)
- **Problem**: During a rare collectible auction, 10,000 bidders watch a live countdown clock and submit bids in the final 5 seconds. If the server has thread scheduling delays, bids arrive late and users complain.
- **Solution**: **Asyncio event loop with Redis pub/sub**. Bids are ingested asynchronously, broadcast to all 10,000 connected WebSocket clients in real-time, and written to the database asynchronously.

### Domain 3: Banking (Payment Gateway Multi-Bank Settlement)
- **Problem**: At midnight, a financial institution reconciles daily merchant settlements by querying 15 partner bank APIs. Each API takes 1.5 seconds to return XML reports. Sequential execution takes over 22 seconds, causing timeouts.
- **Solution**: Using `asyncio.gather()`, all 15 partner bank APIs are queried simultaneously. The entire batch finishes in 1.6 seconds.

---

## 7. Best Practices

### Practice 1: Never Call `time.sleep()` in an Async Function
**When to apply**: Always inside `async def` functions.
**Why**: `time.sleep()` halts the entire operating system thread, freezing the event loop for all users. Always use `await asyncio.sleep()`.

```python
# Bad
async def poll():
    time.sleep(1.0) # Freezes the whole server!

# Good
async def poll():
    await asyncio.sleep(1.0) # Yields to other users
```

---

### Practice 2: Always Use `asyncio.create_task()` to Run Concurrent Background Work
**When to apply**: When starting a job that should run alongside your current function.
**Why**: Calling `await some_coroutine()` directly runs it sequentially. Wrapping it with `asyncio.create_task(some_coroutine())` schedules it concurrently.

```python
# Good Practice
task1 = asyncio.create_task(send_email())
task2 = asyncio.create_task(update_database())
await asyncio.gather(task1, task2)
```

---

### Practice 3: Always Use `asyncio.wait_for()` on External Network Calls
**When to apply**: Whenever calling third-party APIs or remote databases.
**Why**: Networks can drop packets silently. Without a timeout, your task will remain suspended forever, leaking memory.

---

## 8. Top 3 Mistakes & Anti-Patterns

### Mistake 1: Forgetting the `await` Keyword
#### What's the Problem?
Calling a coroutine function without `await`.
#### Why It Happens
Beginners forget that calling an `async def` function does *not* execute it—it only returns a coroutine object!
#### Impact
The function never runs, and Python outputs `RuntimeWarning: coroutine 'my_func' was never awaited`.
#### Incorrect Code
```python
async def save_data():
    print("Data saved!")

async def main():
    save_data()  # BUG: Does NOT run!
```
#### Correct Code
```python
async def main():
    await save_data()  # Runs and prints "Data saved!"
```

---

### Mistake 2: Calling Synchronous Database or HTTP Libraries
#### What's the Problem?
Using `requests.get()` or synchronous `sqlite3` inside an async web server.
#### Why It Happens
Developers import their favorite familiar libraries into a new FastAPI or Asyncio app.
#### Impact
The synchronous call blocks the single thread, destroying the asynchronous performance benefit.
#### Correct Approach
Use asynchronous alternatives:
- Replace `requests` with `httpx` or `aiohttp`.
- Replace `sqlite3` with `aiosqlite`.
- Or offload blocking calls using `await loop.run_in_executor(None, blocking_func)`.

---

### Mistake 3: Catching Base Exception and Swallowing `CancelledError`
#### What's the Problem?
Writing a blanket `except Exception:` or `except BaseException:` that catches `asyncio.CancelledError`.
#### Why It Happens
Trying to catch all errors to prevent crashes.
#### Impact
When the event loop tries to cancel a task or shut down cleanly, the coroutine refuses to stop, causing hangs during server shutdown.
#### Correct Approach
```python
try:
    await do_work()
except asyncio.CancelledError:
    # Always re-raise CancelledError to allow clean task shutdown!
    raise
except Exception as e:
    print(f"Handled error: {e}")
```
