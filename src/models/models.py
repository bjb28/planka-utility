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

    def __repr__(self):
        """Return string representation of an object."""
        return repr(f"{type(self)}: {self.id} - {self.name}")

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

    def insert(self):
        """Return SQL INSERT query for a Project by name."""
        return f"""INSERT INTO project (name) VALUES ('{self.name}')"""

    def load_json(self, json, force=False):
        """Load a JSON into a Project Object.

        Args:
            json (JSON Object): The JSON object to be loaded.
            force (bool, optional): Set to True to over ride any existing attributes. Defaults to False.
        """
        for key, val in json.items():
            if key == "boards":
                for index, board in enumerate(val):
                    # TODO Check if board already exists.
                    val[index] = Board.parse(board)
                setattr(self, key, val)
            elif getattr(self, key) == self._valid_properties[key] or force:
                setattr(self, key, val)

    def select_id(self):
        """Return SQL SELECT query for a Project id by the name."""
        return f"""SELECT id FROM project WHERE name='{self.name}'"""


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

    def insert(self):
        """Return SQL INSERT query for a Board requires project id, name, and position."""
        return f"""
            INSERT INTO
                board (project_id, type, name, position)
            VALUES
                ({self.project_id}, 'kanban', '{self.name}', {self.position})
        """

    def select_id(self):
        """Return SQL SELECT query for a Board id by the name."""
        return f"""SELECT id FROM board WHERE name='{self.name}'"""


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

    def insert(self):
        """Return SQL INSERT query for a List requires board id, name, and position."""
        return f"""
            INSERT INTO
                list (board_id, name, position)
            VALUES
                ({self.board_id}, '{self.name}', {self.position})
        """

    def select_id(self):
        """Return SQL SELECT query for a List id by the name."""
        return f"""SELECT id FROM list WHERE name='{self.name}'"""


class Card(Model):
    """The Card class."""

    _valid_properties: Dict[str, Any] = {
        "id": None,
        "name": None,
        "position": 0,
        "tasks": list(),
        "board_id": None,
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

    def insert(self):
        """Return SQL INSERT query for a Card requires board id, list id, name, and position."""
        return f"""
                    INSERT INTO
                        card (board_id, list_id, name, position)
                    VALUES
                        ({self.board_id}, {self.list_id}, '{self.name}', {self.position})
                """

    def select_id(self):
        """Return SQL SELECT query for a Card id by the name."""
        return f"""SELECT id FROM card WHERE name='{self.name}'"""
