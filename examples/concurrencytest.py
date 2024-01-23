import concurrent.futures
import threading
import queue
import random
import time

def heavy_computation(task):
    # Simulate a heavy computation task
    time.sleep(random.uniform(0.1, 0.5))
    return f"Result of {task}"

def process_future(future, order, result_queue):
    result = future.result()
    result_queue.put((order, result))
    # The result is now only referenced in the queue

def save_result_in_order(result_queue):
    """
    Saves the results from a result queue in the expected order.

    Args:
        result_queue (Queue): The result queue containing the results.

    Returns:
        None
    """
    buffer = {}
    expected_order = 0
    while True:
        order, result = result_queue.get()
        if order is None:  # Signal to stop
            break

        buffer[order] = result

        while expected_order in buffer:
            print(f"Saving {buffer[expected_order]}")
            del buffer[expected_order]
            expected_order += 1
            result_queue.task_done()

tasks = range(10)
result_queue = queue.Queue()

saving_thread = threading.Thread(target=save_result_in_order, args=(result_queue,))
saving_thread.start()

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = []
    for order, task in enumerate(tasks):
        future = executor.submit(heavy_computation, task)
        future.add_done_callback(lambda f, order=order: process_future(f, order, result_queue))
        futures.append(future)

# Wait for all tasks to be submitted and processed
for future in futures:
    future.result()

# Signal the saving thread to finish
result_queue.put((None, None))
saving_thread.join()
