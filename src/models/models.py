"""The models library."""

# Standard Python Libraries
from typing import Any, Dict

POSITION_GAP = 65535


class Model(object):
    """The Model class."""

    _valid_properties: Dict[str, Any] = dict()

    @classmethod
    def _is_builtin(cls, obj):
        return isinstance(obj, (int, float, str, list, dict, bool))

    def as_dict(self):
        """Return a dict representation of the resource."""
        result = {}
        for key in self._valid_properties:
            val = getattr(self, key)
            # Parse custom classes
            if val and not Model._is_builtin(val):
                val = val.as_dict()
            # Parse lists of objects
            elif isinstance(val, list):
                # Only call as_dict if item isn't built in type.
                for i in range(len(val)):
                    if Model._is_builtin(val[i]):
                        continue
                    val[i] = val[i].as_dict()
            # Add boolean values
            elif isinstance(val, bool):
                result[key] = val

            # Add item if it's not None
            if val:
                result[key] = val

        return result

    @classmethod
    def parse(cls, json):
        """Parse a JSON object into a model instance."""
        raise NotImplementedError


class Project(Model):
    """The Project class."""

    _valid_properties: Dict[str, Any] = {
        "id": None,
        "name": None,
        "boards": list(),
    }

    def __init__(self, **kwargs):
        """Create a new project instance."""
        for key, default in Project._valid_properties.items():
            setattr(self, key, kwargs.get(key, default))

    @classmethod
    def parse(cls, json):
        """Parse project json."""
        project = cls()
        for key, val in json.items():
            if key == "boards":
                for index, board in enumerate(val):
                    val[index] = Board.parse(board)

            if key in cls._valid_properties:
                setattr(project, key, val)
        return project


class Board(Model):
    """The Board class."""

    _valid_properties: Dict[str, Any] = {
        "id": None,
        "name": None,
        "position": 0,
        "lists": list(),
        "project_id": None,
    }

    def __init__(self, **kwargs):
        """Create a new board instance."""
        for key, default in Board._valid_properties.items():
            setattr(self, key, kwargs.get(key, default))

    @classmethod
    def parse(cls, json):
        """Parse board json."""
        board = cls()
        for key, val in json.items():
            if key == "lists":
                for index, _list in enumerate(val):
                    val[index] = List.parse(_list)

            if key in cls._valid_properties:
                setattr(board, key, val)

        return board


class List(Model):
    """The List class."""

    _valid_properties: Dict[str, Any] = {
        "id": None,
        "name": None,
        "position": 0,
        "cards": list(),
        "board_id": None,
    }

    def __init__(self, **kwargs):
        """Create a new list instance."""
        for key, default in List._valid_properties.items():
            setattr(self, key, kwargs.get(key, default))

    @classmethod
    def parse(cls, json):
        """Parse list json."""
        _list = cls()
        for key, val in json.items():
            if key == "cards":
                for index, card in enumerate(val):
                    val[index] = Card.parse(card)

            if key in cls._valid_properties:
                setattr(_list, key, val)

        return _list


class Card(Model):
    """The Card class."""

    _valid_properties: Dict[str, Any] = {
        "id": None,
        "name": None,
        "position": 0,
        "tasks": list(),
        "list_id": None,
    }

    def __init__(self, **kwargs):
        """Create a new card instance."""
        for key, default in Card._valid_properties.items():
            setattr(self, key, kwargs.get(key, default))

    @classmethod
    def parse(cls, json):
        """Parse card json."""
        card = cls()
        for key, val in json.items():
            if key in cls._valid_properties:
                setattr(card, key, val)

        return card
