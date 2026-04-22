import sys
import os

print("PID:", os.getpid())

def test_import(modname):
    print(f"Testing {modname}...", flush=True)
    try:
        __import__(modname)
        print(f"  {modname} OK", flush=True)
    except BaseException as e:
        print(f"  {modname} FAILED: {type(e).__name__}: {e}", flush=True)

test_import("os")
test_import("sys")
test_import("pydantic")
test_import("pydantic_core")
test_import("langchain_core")
test_import("langchain_community")
test_import("langchain")
test_import("langchain.tools")
print("Done.", flush=True)
