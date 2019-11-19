#!/usr/bin/env python
# -*- coding: utf-8 -*-
import logging


def init_logger(module_name):
    file_name = 'test.log'

    # Create a logger for this module
    logger = logging.getLogger(module_name)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(fmt='%(asctime)s.%(msecs)03d : '
                                      '%(levelname)-8s : '
                                      '%(name)-15s : '
                                      '%(lineno)d : '
                                      '%(message)s',
                                  datefmt='%Y-%m-%d %H:%M:%S')

    # Create a file handler
    file_handler = logging.FileHandler(file_name)
    file_handler.setFormatter(formatter)

    # Create a stream handler
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)

    # Bind it to a logger
    logger.addHandler(file_handler)
#    logger.addHandler(stream_handler)
    return logger
