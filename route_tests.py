import subprocess, os, sys

# 1. Find files changed in the last commit
out = subprocess.run(
    ["git", "diff", "--name-only", "HEAD~1"],
    capture_output=True, text=True
).stdout.split()

# 2. Dynamically pick matching tests
tests = set()
for f in out:
    name = os.path.basename(f)
    if f.startswith("src/") and name.endswith(".py") and name != "__init__.py":
        test_file = f"tests/test_{name}"
        if os.path.exists(test_file):
            tests.add(test_file)
    elif f.startswith("tests/") and f.endswith(".py"):
        tests.add(f)

# 3. Run the subset, or everything if nothing matched
if tests:
    print("Running only:", sorted(tests))
    cmd = [sys.executable, "-m", "pytest", *sorted(tests)]
else:
    print("No specific match, running all tests")
    cmd = [sys.executable, "-m", "pytest"]

sys.exit(subprocess.run(cmd).returncode)
