# https://stackabuse.com/creating-executable-files-from-python-scripts-with-py2exe/
from distutils.core import setup # Need this to handle modules
import py2exe 
#import math # We have to import all modules used in our program
import argparse
import datetime
import subprocess
import json
import logging
import os
import signal
import sys
import time
import psutil
import random
import importlib

ROOT = os.path.normpath(os.path.join(os.path.abspath(__file__), ".."))

import common
import logger

setup(console=['core_bouncer.py']) # Calls setup function to indicate that we're dealing with a single console application