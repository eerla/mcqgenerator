import logging
import os
from datetime import datetime

_FILENAME = datetime.now().strftime('%m_%d_%Y_%H_%M_%S')
LOG_FILE_NAME = f"mcqg_{_FILENAME}.log"
LOG_PATH = os.path.join(os.getcwd(),"logs")

if not os.path.exists(LOG_PATH):
     os.makedirs(LOG_PATH)

LOG_FILE_PATH = os.path.join(LOG_PATH, LOG_FILE_NAME)

logging.basicConfig(level=logging.INFO,
        filename=LOG_FILE_PATH,
        format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s")

