import logging
import sys

from testrail_reporting.app import app

log = logging.getLogger(__name__)


def setup_logging():
    logging_format = "[%(asctime)s] - %(name)s - %(levelname)s - %(message)s"
    logging.basicConfig(stream=sys.stdout,
                        level=logging.DEBUG,
                        format=logging_format)
    logging.getLogger("requests").setLevel(logging.ERROR)
    logging.getLogger("iso8601").setLevel(logging.ERROR)


setup_logging()

app.debug = app.config['DEBUG']
app.run(host="127.0.0.1", port=5000, debug=True)
