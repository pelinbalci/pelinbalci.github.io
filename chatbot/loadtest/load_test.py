from gradio_client import Client
import threading, time

SPACE = "pelinbalci/pelin-notes-chat"
API_NAME = "/chat"

client = Client(SPACE)

def worker(i):
    try:
        out = client.predict("Explain neural networks", api_name=API_NAME)
        print(f"User {i}: OK")
    except Exception as e:
        print(f"User {i}: FAIL -> {type(e).__name__}: {repr(e)}")

threads = []
N = 40

for i in range(N):
    t = threading.Thread(target=worker, args=(i,))
    t.start()
    threads.append(t)
    time.sleep(0.1)  # smaller = more “same second” burst

for t in threads:
    t.join()
