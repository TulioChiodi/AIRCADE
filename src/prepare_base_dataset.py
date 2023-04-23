import subprocess
import shutil
import zipfile
from pathlib import Path
import soundfile as sf

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

# remove .ini files
for filename in dst_dir.glob("**/*.ini"):
    filename.unlink()

# remove silence from the beginning of RIR 64
rir_64 = dst_dir / "rir" / "rir_0064.wav"

start_time = 0.82
start_samples = int(start_time * 48000)

y, sr = sf.read(rir_64, start=start_samples)
sf.write(rir_64, y, sr)

