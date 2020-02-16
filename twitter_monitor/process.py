""" Process tweet application """
import datetime
import json
import zmq

from config import STORE_SCREENSHOTS, EXPORT_ROOT, QUEUE_PORT
from utilities import get_screenshot


def process_msg(msg):
    msg_json = json.loads(msg.decode("utf-8"))
    status_id = msg_json["id"]

    date_str = f"{datetime.date.today().isoformat()}"
    tweet_path = EXPORT_ROOT / date_str / f"{status_id}"
    tweet_path.mkdir(exist_ok=True, parents=True)
    with open(tweet_path / f"{status_id}.json", "ab") as fout:
        json.dump(status_id, fout)

    if STORE_SCREENSHOTS:
        get_screenshot(status_id, tweet_path)


def main():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind(f"tcp://*:{QUEUE_PORT}")

    while True:
        #  Wait for next request from client
        message = socket.recv()
        socket.send(b"")
        print("Received request: %s" % message.decode("utf-8"))


if __name__ == "__main__":
    main()
