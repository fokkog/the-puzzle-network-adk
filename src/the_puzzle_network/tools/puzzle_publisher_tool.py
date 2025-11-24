"""Publisher tools for game output and structure."""

from ..logging import get_logger


logger = get_logger(__name__)


class PuzzlePublisherTool:
    def __init__(self) -> None:
        pass

    def publish(self, level: str, html_content: str) -> dict:
        """Sends out mail with the game content to the appropriate distribution list.
        Actually to avoid the mail setup complexities, this function will just log the parameters.

        Args:
            level: The level of the game, either 'easy', 'medium', or 'hard'.
            html_content: The HTML-formatted puzzle.

        Returns:
            Dictionary with status and number of deliveries.
            Success: {"status": "success", "number of deliveries": 20}
            Error: {"status": "error", "error_message": "publishing failed"}
        """

        logger.info(">>>>>>>>>>>>>> Sending out puzzle START <<<<<<<<<<<<")
        logger.info("Level:\n%s", level)
        logger.info("HTML Content:\n%s", html_content)
        logger.info("<<<<<<<<<<<<<< Sending out puzzle  END  <<<<<<<<<<<<")
        return {"status": "success", "number of deliveries": 20}
