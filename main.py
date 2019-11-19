#!/usr/bin/env python
# -*- coding: utf-8 -*-
import log
from flask import Flask
from flask_restful import reqparse, Api, Resource
import json
import scraper
import tempfile
import sys
import os

logger = log.init_logger(__name__)


def mutex():
    tempdir = tempfile.gettempdir()
    lockfile = os.path.join(tempdir, 'kross.lock')

    try:
        if os.path.isfile(lockfile):
            os.unlink(lockfile)
    except WindowsError as e:
        logger.error("Launch failed: An instance is already running.")
        sys.exit(1)

    with open(lockfile, 'wb') as lock_handle:
        # Run the application here
        main()
    os.unlink(lockfile)


class ScraperApi(Resource):
    def __init__(self, **kwargs):
        self.parser = kwargs['parser']

    def post(self):
        args = self.parser.parse_args()
        args = dict(args)  # Convert to dict

        # Run the scraper
        result_dict = scraper.scraper(args)
        return result_dict, 200


def main():
    app = Flask(__name__)
    api = Api(app)

    @app.route("/")
    def entry():
        return 'Kross Scraper v.0.2.0'

    # Read file 'default.json'
    with open('default.json', 'r', encoding='utf-8') as json_file:
        json_string = json_file.read()
    json_string = json_string.replace("\\", "\\\\")
    json_obj = json.loads(json_string)

    # Create parser for POST request
    parser = reqparse.RequestParser()
    for key in json_obj:
        parser.add_argument(key, type=str)

    api.add_resource(ScraperApi, '/enote/fetch', resource_class_kwargs={'parser': parser})

    host = '0.0.0.0'
    port = '3001'
    logger.info(f"Server starts at port {port}")
    app.run(host=host, port=port)


if __name__ == '__main__':
    mutex()
