import logging
import json

#
# def logging_override(name: str, extra: dict):
#     logger = logging.getLogger(name)
#     logger.setLevel(logging.INFO)
#     stream_handler = logging.StreamHandler()
#     basic_dict = {"time": "%(asctime)s", "level": "%(levelname)s", "message": "%(message)s"}
#     full_dict = {**basic_dict, **extra}
#     stream_formatter = logging.Formatter(json.dumps(full_dict))
#     stream_handler.setFormatter(stream_formatter)
#     if not logger.handlers:
#         logger.addHandler(stream_handler)
#     logger.handlers[0] = stream_handler
#     logger = logging.LoggerAdapter(logger, extra)
#     return logger
#
#
# def main():
#     logging.debug("Sending Email to username: 'Jack Sparrow' regarding server_ip: '192.168.1.2'")
#     extra = {'server_ip': '192.168.1.2', 'username': 'Jack Sparrow'}
#     logger = logging_override("json", extra)
#     logger.info("Sending Email to username: 'Jack Sparrow' regarding server_ip: '192.168.1.2'")
#
# if __name__ == '__main__':
    #main()


import ecs_logging

logger = logging.getLogger("app")
logger.setLevel(logging.DEBUG)

# Add an ECS formatter to the Handler
handler = logging.StreamHandler()
handler.setFormatter(ecs_logging.StdlibFormatter())
logger.addHandler(handler)

# Emit a log!
logger.debug("Sending Email to username: 'Jack Sparrow' regarding server_ip: '192.168.1.2'", extra={"http.request.method": "get"})