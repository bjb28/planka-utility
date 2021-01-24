"""pytest plugin configuration.

https://docs.pytest.org/en/latest/writing_plugins.html#conftest-py-plugins
"""

# Standard Python Libraries
import json

# Third-Party Libraries
import pytest

# Custom Libraries
from models.models import Board, Card, List, Project

""" Proeject Fixtures """


@pytest.fixture
def project_json(board_json):
    """Return a Project JSON."""
    project_str = json.dumps({"id": 1, "name": "Test Project", "boards": [board_json]})
    return json.loads(project_str)


@pytest.fixture
def project_object(board_object):
    """Return a Project object."""
    return Project(id=1, name="Test Project", boards=[board_object])


@pytest.fixture
def board_json(list_json):
    """Return a Board JSON."""
    board_str = json.dumps(
        {
            "id": 1,
            "name": "Test Board 1",
            "lists": [list_json],
            "position": 0,
            "project_id": 1,
        }
    )
    return json.loads(board_str)


@pytest.fixture
def board_object(list_object):
    """Return a Board object."""
    return Board(
        id=1, name="Test Board 1", lists=[list_object], position=0, project_id=1
    )


@pytest.fixture
def list_json(card_json):
    """Return a List JSON."""
    list_str = json.dumps(
        {
            "id": 1,
            "name": "Test List 1",
            "cards": [card_json],
            "position": 0,
            "board_id": 1,
        }
    )
    return json.loads(list_str)


@pytest.fixture
def list_object(card_object):
    """Return a List Object."""
    return List(id=1, name="Test List 1", cards=[card_object], position=0, board_id=1)


@pytest.fixture
def card_json():
    """Return a Card JSON."""
    card_str = json.dumps(
        {
            "id": 1,
            "name": "Test Card 1",
            "tasks": ["Task 1", "Task 2"],
            "position": 0,
            "list_id": 1,
        }
    )
    return json.loads(card_str)


@pytest.fixture
def card_object():
    """Return a Card Object."""

    return Card(
        id=1, name="Test Card 1", tasks=["Task 1", "Task 2"], position=0, list_id=1
    )
