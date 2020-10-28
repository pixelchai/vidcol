import logging
import os
import sys
from datetime import datetime

# set up logging

PATH_LOGGING = "logs"
logger = logging.getLogger("webmcol")

if len(logger.handlers) <= 0:
    os.makedirs(PATH_LOGGING, exist_ok=True)

    fh = logging.FileHandler(filename=os.path.join(PATH_LOGGING, datetime.utcnow().strftime("%Y_%m_%d.log")))
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter(
        "%(asctime)s - %(name)s (%(module)s %(pathname)s:%(lineno)s) - %(levelname)s - %(message)s"
    ))

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.DEBUG)
    ch.setFormatter(logging.Formatter("%(asctime)s - %(levelname)s - %(message)s"))

    logger.setLevel(logging.DEBUG)

    logger.addHandler(fh)
    logger.addHandler(ch)