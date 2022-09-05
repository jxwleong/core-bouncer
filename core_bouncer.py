# Contact: jxwleong/xleong
import subprocess
import json
import os

command = "bin/linux/core_type" if os.name == "posix" else "bin/windows/core_type.exe" if os.name == "nt" else "Not supported OS"
core_mapping_process = subprocess.run(command, capture_output=True)
core_mapping_dict = json.loads(core_mapping_process.stdout.decode("utf-8"))
print(core_mapping_dict)
