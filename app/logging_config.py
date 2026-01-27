import watchtower, logging

def configure_logging(app):
    logger = logging.getLogger("security.audit")
    logger.setLevel(logging.INFO)

    if not logger.handlers:
        handler = watchtower.CloudWatchLogHandler(
            log_group_name="aeblog/app"
        )

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(name)s - %(message)s"
        )
        handler.setFormatter(formatter)

        logger.addHandler(handler)

    logger.info("security logger initialized")
