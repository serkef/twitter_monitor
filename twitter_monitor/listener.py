""" Custom stream listener """

import json
import logging
from time import sleep

from tweepy import StreamListener
import zmq

from config import QUEUE_PORT


class Listener(StreamListener):
    def __init__(self):
        super().__init__()
        self.zmq_context = zmq.Context()
        self.zmq_socket = self.zmq_context.socket(zmq.REQ)
        self.zmq_socket.connect(f"tcp://localhost:{QUEUE_PORT}")

    def on_status(self, status):
        """ on_status callback. Filters out Retweets and comments"""

        logger = logging.getLogger(f"{__name__}.Listener.on_status")
        logger.info(f"Received status: {status.id}")
        obj = json.dumps(status._json, ensure_ascii=False, check_circular=False)
        self.zmq_socket.send(obj.encode("utf-8"))
        self.zmq_socket.recv()

    def on_error(self, status_code):
        """ on_error callback. Works to handle exceptions"""

        logger = logging.getLogger(f"{__name__}.Listener.on_error")
        logger.error(f"Got error: {status_code}")
        if status_code in {406, 420}:
            logger.info("Sleeping...")
            sleep(60)

        return False
