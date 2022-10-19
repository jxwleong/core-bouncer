# Contact: jxwleong/xleong
import argparse
import subprocess
import json
import logging
import os
import signal
import sys
import time
import psutil
import random

from common import core_type_def
from common import core_type_command
import logger

logger = logging.getLogger(__name__)
ROOT = os.path.normpath(os.path.join(os.path.abspath(__file__), ".."))
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
        if "0x20" in core_type:
            atom_list.append(core_id)
        elif "0x40" in core_type:
            core_list.append(core_id)

    return atom_list, core_list

def get_switch_iteration(total_timeout, switch_time):
    return int(total_timeout/switch_time)

if __name__ == "__main__":
    arg_parser = argparser_init()
    process_arg(arg_parser)
    print(argtable)
    # Make full path to the binaries instead of relative path
    full_command = os.path.join(ROOT, command)
    core_mapping_process = subprocess.run(full_command, capture_output=True)
    core_mapping_dict = json.loads(core_mapping_process.stdout.decode("utf-8"))
    
    # mock
    core_mapping_dict = {
            "core_0":"Atom (0x20)",
            "core_1":"Atom (0x20)",
            "core_2":"Atom (0x20)",
            "core_3":"Atom (0x20)",
            "core_4":"Core (0x40)",
            "core_5":"Core (0x40)",
            "core_6":"Core (0x40)",
            "core_7":"Core (0x40)"
    }

    atom_list, core_list = get_core_list(core_mapping_dict)
    if 'Unknown type (0x0)' in core_mapping_dict.values():      
        print("Not Hybrid Core Config detected!")
    else:
        print("Hybrid Core detected!")

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
        print(f"Affinitize process {psutil_app_process} to core {random_big_core}")
        psutil_app_process.cpu_affinity([random_big_core])
        current_core = "core"
        for iteration in range(iterations):
            time.sleep(argtable["switch_time"])
            if current_core == "core":
                next_core = random.choice(atom_list)
            elif current_core == "atom":
                next_core = random.choice(core_list)
            print(f"Affinitize process {psutil_app_process} to core {next_core}")
            psutil_app_process.cpu_affinity([next_core])


    os.kill(app_process.pid, signal.SIGINT)