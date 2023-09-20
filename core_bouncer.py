# Contact: jxwleong/xleong
# pyinstaller .\core_bouncer.py --onefile --paths="path\cpuid.py\lib;path\cpuid.py"
import argparse
import datetime
import subprocess
import json
import logging
import os
import signal
import sys
import time
import random

ROOT = os.path.normpath(os.path.join(os.path.abspath(__file__), ".."))
LIB = os.path.normpath(os.path.join(ROOT, "lib"))

sys.path.append(ROOT)
sys.path.append(LIB)

import psutil
import logger
from common import core_type_def
from common import core_type_command


logger = logging.getLogger(__name__)
command = core_type_command[os.name]

argtable = {
    "application": "notepad.exe",
    "total_time": None,
    "switch_time": None
}


def argparser_init():
    """
    Initliaze the argparser 
    """
    parser = argparse.ArgumentParser(
        description="Use to run application and switch the process between big and atom core. NOTE: Only work on hybrid config for now\n"
                    "Contact: xleong",
        formatter_class=argparse.RawTextHelpFormatter
    )
    parser.add_argument('-t', '--switch_time', type=int,
                        help=f"""\
                            Time for the thread to bounce :P

                            Default: None
                             """)

    parser.add_argument('-tt', '--total_time', type=int,
                        help=f"""\
                             Total time for the application to run in seconds

                             Default: None
                             """)
    
    parser.add_argument('-a', '--application', type=str,
                        help=f"""\
                             Application to run

                             Default: None
                            """)
    return parser


def process_arg(parser, args_dict=argtable):
    """
    Process the arguments and store the respective value to
    argtable dictionary
    """

    if not len(sys.argv) > 1:
        logger.error("No argument are passed into emon_checker! Use '-h' argument to find out more")
        sys.exit(1)
        
    args = parser.parse_args()
    args_dict = vars(args)

    for arg, value in args_dict.items():
        if value is not None:
            argtable[arg] = value

def get_core_list(core_mapping_dict):
    atom_list = []
    core_list = []
    for core_id, core_type in enumerate(core_mapping_dict.values()):
        if "atom" in core_type.lower():
            atom_list.append(core_id)
        elif "core" in core_type.lower():
            core_list.append(core_id)

    return atom_list, core_list

def get_switch_iteration(total_timeout, switch_time):
    return int(total_timeout/switch_time)

if __name__ == "__main__":
    arg_parser = argparser_init()
    process_arg(arg_parser)
    logger.info(argtable)

    # Some issue with pyinstaller --onefile as it change the executable
    # path into some temp folder instead of the ROOT of the repo
    core_mapping_process = subprocess.run(command, capture_output=True)
    core_mapping_dict = json.loads(core_mapping_process.stdout.decode("utf-8"))

    atom_list, core_list = get_core_list(core_mapping_dict)
    logger.info(f"Atom core list: {atom_list}")
    logger.info(f"Big core list: {core_list}")

    if 'Unknown type (0x0)' in core_mapping_dict.values():      
        logger.warning("Not Hybrid Core Config detected!")
    else:
        logger.info("Hybrid Core detected!")

    iterations = get_switch_iteration(argtable["total_time"], argtable["switch_time"])
    start_time_in_seconds = int(time.time())
    expect_end_time_in_seconds = start_time_in_seconds + argtable["total_time"]
    
    application_command = argtable["application"].split(" ")
    while int(time.time()) < expect_end_time_in_seconds:
        app_process = subprocess.Popen(application_command)
        psutil_app_process = psutil.Process(pid=app_process.pid)
        current_process_affinity = psutil_app_process.cpu_affinity()
        
        # Start with big core only first then atom       
        random_big_core = random.choice(core_list)
        logger.info(f"{datetime.datetime.now()} Affinitize process {psutil_app_process} to core {random_big_core}")
        psutil_app_process.cpu_affinity([random_big_core])
        current_core = "core"
        for iteration in range(iterations):
            time.sleep(argtable["switch_time"])
            if current_core == "core":
                next_core = random.choice(atom_list)
                current_core = "atom"  # Not nice but its work..
            elif current_core == "atom":
                next_core = random.choice(core_list)
                current_core = "core"
            logger.info(f"{datetime.datetime.now()} Affinitize process {psutil_app_process} to core {next_core}")
            psutil_app_process.cpu_affinity([next_core])
            

    os.kill(app_process.pid, signal.SIGINT)
