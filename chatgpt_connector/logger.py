import functools
import json
import logging
import logging.config
import os
from datetime import datetime


@functools.lru_cache()
def get_logger() -> logging.Logger:
    with open(os.path.join(os.path.dirname(__file__), "logger.json")) as f:
        log_conf = json.load(f)

    # ファイル名をタイムスタンプで作成
    log_conf["handlers"]["fileHandler"]["filename"] = os.path.join(
        os.path.dirname(__file__),
        "..",
        "logs",
        "{}.logs".format(datetime.utcnow().strftime("%Y%m%d%H%M%S")),
    )

    logging.config.dictConfig(log_conf)

    logger = logging.getLogger("gpt_logger")
    return logger
