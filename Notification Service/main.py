from fastapi import FASTAPI, Request
from fastapi.responses import JSONResponse
from pydnatic import BaseModel, ValidationError
import logging
import os
'''Логирование в файл и в консоль'''
LOG_FILE = "notofication.log"

logger = logging.getLogger(""
