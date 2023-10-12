import time
import threading
import sys

stop_event = threading.Event()


# Function to update and display the stopwatch
def update_stopwatch():
    start_time = time.time()
    while not stop_event.is_set():
        elapsed_time = time.time() - start_time
        sys.stdout.write(f"\rElapsed time: {elapsed_time:.1f} seconds")
        sys.stdout.flush()
        time.sleep(0.1)


def stopwatch(func, *args, **kwargs):
    # Create an event to signal the stopwatch thread to stop when the function finishes
    stop_event = threading.Event()

    # Start the stopwatch thread
    stopwatch_thread = threading.Thread(target=update_stopwatch)
    stopwatch_thread.start()

    # Call your function
    result = func(*args, **kwargs)

    # Signal the stopwatch thread to stop
    stop_event.set()

    # Wait for the stopwatch thread to finish
    stopwatch_thread.join()

    return result
