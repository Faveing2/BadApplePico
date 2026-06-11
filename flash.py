import subprocess
from pathlib import Path

projectPath = "pico/"
projectFiles = [
    "main.py",
    "epd.py",
    "video.bin"
]

try:
    subprocess.run(
        ["mpremote", "rm", "-rf", ":/"],
        check=True
    )
except subprocess.CalledProcessError as e:
    if e.returncode == 1:
        print("Erased Virtual Filesystem")
    else:
        print(e.output)
        
#### Write Project files
for file in projectFiles:
    try:
        subprocess.run(
            ["mpremote", "cp", projectPath+file, ":/"+file],
            check=True
        )
    except subprocess.CalledProcessError as e:
        print(e.output)

### Write data

# subprocess.run(
#     ["mpremote", "mkdir", "data"],
#     check=True
# )

# dir_path = Path("data/")
# #files = sorted([f.name for f in dir_path.iterdir() if f.is_file()])[0:99]

# files = [str(idx)+".bin" for idx in range(0,4000)]

# #print(files)
# for file in files:
#     #print(file)
#     # if "210.bin" != file:
#     #     continue

#     try:
#         subprocess.run(
#             ["mpremote", "cp", "data/"+file, ":/data/"+file],
#             check=True
#         )
#     except subprocess.CalledProcessError as e:
#         print(e.output)