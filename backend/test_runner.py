from google.adk.runners import Runner
import inspect

print("=" * 60)
print("Runner Methods")
print("=" * 60)

for method in dir(Runner):
    if not method.startswith("_"):
        print(method)

print("=" * 60)