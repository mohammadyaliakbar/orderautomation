import logging

from app.logger import setup_logging
from app.notifications.base import Notifier

setup_logging()
logger = logging.getLogger(__name__)


class ConsolNotifier(Notifier):
    async def send(self, message) -> None:
        logger.info(f"[NOTIFICATION]\n{message}")
