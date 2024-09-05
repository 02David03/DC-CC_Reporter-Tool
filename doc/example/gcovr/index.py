import subprocess
import os

# Compile the test program
test_compile_command = [
    "gcc",
    "-fprofile-arcs", "-ftest-coverage",
    "-o", "doc/example/gcovr/equations/output/test",
    "doc/example/gcovr/equations/tests.c", "doc/example/gcovr/equations/equations.c"
]

subprocess.run(test_compile_command, check=True)

# Step 2: Run the tests
subprocess.run(["doc/example/gcovr/equations/output/test"], check=True)

# Step 3: Generate the coverage report in HTML format
gcovr_command = [
    "gcovr",
    "-r", ".",
    "--html", "--html-nested",
    "-o", "doc/example/gcovr/analysis/coverage.html"
]
subprocess.run(gcovr_command, check=True)

# Optionally, you can open the HTML report in the default web browser
print("Opening the coverage report...")
subprocess.run(["xdg-open", "doc/example/gcovr/analysis/coverage.html"] if os.name == 'posix' else ["start", "doc/example/gcovr/analysis/coverage.html"], shell=True)