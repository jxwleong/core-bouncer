# Contact: jxwleong/xleong
import subprocess
import json
import logging
import os

from common import core_type_def
from common import core_type_command
import logger

logger = logging.getLogger(__name__)
ROOT = os.path.normpath(os.path.join(os.path.abspath(__file__), ".."))
command = core_type_command[os.name]

# Make full path to the binaries instead of relative path
full_command = os.path.join(ROOT, command)
core_mapping_process = subprocess.run(full_command, capture_output=True)
core_mapping_dict = json.loads(core_mapping_process.stdout.decode("utf-8"))

if 'Unknown type (0x0)' in core_mapping_dict.values():      
    print("Not Hybrid Core Config detected!")
else:
    print("Hybrid Core detected!")

print(core_mapping_dict)
