import subprocess
import shutil
import zipfile
from pathlib import Path

command = "zenodo_get 10.5281/zenodo.7818761"
subprocess.call(command, shell=True)

src_dir = Path(".")
dst_dir = Path("data/dataset_base")
dst_dir.mkdir(parents=True, exist_ok=True)

filenames = [
    "guitar.zip",
    "song.zip",
    "speech.zip",
    "rir.zip",
    "metadata.zip",
    "md5sums.txt"
]

# move the files to the destination directory
for filename in filenames:
    shutil.move(src_dir / filename, dst_dir / filename)

# unzip the files
for filename in filenames:
    if filename.endswith(".zip"):
        with zipfile.ZipFile(dst_dir / filename, "r") as zip_ref:
            zip_ref.extractall(dst_dir)

# remove the zip files
for filename in filenames:
    if filename.endswith(".zip"):
        (dst_dir / filename).unlink()