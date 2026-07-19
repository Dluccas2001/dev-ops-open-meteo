import shutil
from pathlib import Path

TARGETS = [Path("data/raw"), Path("data/processed"), Path("models"), Path("mlruns")]


def main() -> None:
    for target in TARGETS:
        if target.exists():
            shutil.rmtree(target)
        target.mkdir(parents=True, exist_ok=True)
    print("Local generated outputs cleaned.")


if __name__ == "__main__":
    main()
