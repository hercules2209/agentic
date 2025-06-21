from functions.run_python_file import run_python_file

if __name__ == "__main__":
    cases = [
      ("calculator", "main.py"),
      ("calculator", "tests.py"),
      ("calculator", "../main.py"),
      ("calculator", "nonexistent.py")
    ]

    for workdir, target in cases:
        result = run_python_file(workdir, target)
        print(f"run_python_file({workdir!r}, {target!r}) →")
        print(result)
        print("-" * 60)
