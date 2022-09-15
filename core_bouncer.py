# Contact: jxwleong/xleong
import subprocess
import json
import os

ROOT = os.path.normpath(os.path.join(os.path.abspath(__file__), ".."))
command = "bin/linux/core_type" if os.name == "posix" else "bin\windows\core_type.exe" if os.name == "nt" else "Not supported OS"

# Make full path to the binaries instead of relative path
full_command = os.path.join(ROOT, command)
core_mapping_process = subprocess.run(full_command, capture_output=True)
core_mapping_dict = json.loads(core_mapping_process.stdout.decode("utf-8"))

if 'Unknown type (0x0)' in core_mapping_dict.values():      
    print("Not Hybrid Core Config detected!")
else:
    print("Hybrid Core detected!")

print(core_mapping_dict)
