# Contact: jxwleong/xleong
import cpuid
import psutil
import json

import logging

from common import core_type_def
import logger

logger = logging.getLogger(__name__)



def get_core_type():
    cpu = cpuid.CPUID()
    regs = cpu(0x1a, 0)
    core_type = "Atom" if regs[0] >> 24 == core_type_def["atom"] else "Core" if regs[0] >> 24 == core_type_def["core"] else f"Unknown type ({hex(regs[0] >> 24)})"
    return core_type

total_core_count = psutil.cpu_count()


def main():
    core_mapping = {}
    for core in range(total_core_count):
        current_process = psutil.Process()
    
        # Set affinity
        current_process.cpu_affinity([core])  # expecting list terable
        #print(f"Core{core}------------->{get_core_type()}")
        core_mapping[f"core_{core}"] = get_core_type()

    logger.info(json.dumps(core_mapping, indent="\t"))

    
if __name__ == "__main__":
    main()
