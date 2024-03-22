import os
from collections.abc import Sequence
from pathlib import Path

BASE_DIR = Path(__file__).parent.resolve()
DOTENVS_DIR = os.path.join(BASE_DIR, ".envs")
DOTENV_FILES = [
    Path(DOTENVS_DIR, ".django"),
    Path(DOTENVS_DIR, ".postgres"),
]
DOTENV_FILE = BASE_DIR / ".env"


def merge(
    output_file: Path,
    files_to_merge: Sequence[Path],
) -> None:
    merged_content = ""
    for merge_file in files_to_merge:
        merged_content += merge_file.read_text()
        merged_content += os.linesep
    output_file.write_text(merged_content)


if __name__ == "__main__":
    merge(DOTENV_FILE, DOTENV_FILES)
