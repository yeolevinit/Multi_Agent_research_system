import sys
import traceback

print("Starting debug import script...", flush=True)

try:
    print("Attempting to import langchain.tools...", flush=True)
    from langchain.tools import tool
    print("Successfully imported langchain.tools!", flush=True)
except SystemExit as e:
    print(f"Caught SystemExit! Code: {e.code}", flush=True)
    traceback.print_exc()
except BaseException as e:
    print(f"Caught an exception: {type(e).__name__}: {e}", flush=True)
    traceback.print_exc()
else:
    print("Finished with no exceptions.", flush=True)

print("Exiting debug script.", flush=True)
