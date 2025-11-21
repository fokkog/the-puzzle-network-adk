"""Basic tests for tools module."""

import pytest

from the_puzzle_network.tools.publisher_tool import PublisherTool


def test_dummy_publishing():
    publisher = PublisherTool()
    result = publisher.publish("easy", "<html>Test Content</html>")
    assert result.get("status") == "success"
    assert result.get("number of deliveries") == 20


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
