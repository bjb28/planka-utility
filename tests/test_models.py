#!/usr/bin/env pytest -vs
"""Tests for Models."""

# Custom Libraries
from models.models import Board, Card, List, Project


class TestBaseModel:
    """Test base model."""

    def test_model_repr(self, board_object):
        """Test proper string returned by __repr__"""
        assert (
            str(repr(board_object))
        ) == "\"<class 'models.models.Board'>: 1 - Test Board 1\""


class TestModelLoad:
    """Test load method for each class."""

    def test_project_load(self, project_json):
        """Test loading a project into an new project object."""
        new_project = Project()
        new_project.load_json(project_json)
        assert new_project.as_dict() == project_json

    def test_project_load_existing_attributes(self, project_json):
        # Create instance of project with a name.
        new_project = Project(name="Test Full Project")
        new_project.load_json(project_json)

        # Update JSON to expected.
        project_json["name"] = "Test Full Project"

        assert new_project.as_dict() == project_json


class TestParse:
    """Test parsers for each class."""

    def test_project_parse(self, project_object, project_json):
        """Test parsing of project JSON."""
        assert project_object.as_dict() == Project.parse(project_json).as_dict()

    def test_project_parse_fail(self, project_object, project_json):
        """Test a failing parsing of a project JSON."""
        project_json["boards"] = [{"test": 0}]
        assert project_object.as_dict() != Project.parse(project_json).as_dict()

    def test_board_parse(self, board_object, board_json):
        """Test parsing of board JSON."""
        assert board_object.as_dict() == Board.parse(board_json).as_dict()

    def test_board_parse_fail(self, board_object, board_json):
        """Test parsing of board JSON will raise attribute error."""
        board_json["lists"] = [{"test": 0}]
        assert board_object.as_dict() != Board.parse(board_json).as_dict

    def test_list_parse(self, list_object, list_json):
        """Test parsing of list JSON."""
        assert list_object.as_dict() == List.parse(list_json).as_dict()

    def test_list_parse_fail(self, list_object, list_json):
        """Test parsing of list JSON will raise attribute error."""
        list_json["cards"] = [{"test": 0}]
        assert list_object.as_dict() != List.parse(list_json).as_dict

    def test_card_parse(self, card_object, card_json):
        """Test parsing of card JSON."""
        assert card_object.as_dict() == Card.parse(card_json).as_dict()

    def test_card_parse_fail(self, card_object, card_json):
        """Test parsing of card JSON will raise attribute error."""
        card_json["tasks"] = ["1"]
        assert card_object.as_dict() != Card.parse(card_json).as_dict


class TestSQLQuery:
    """Test the insert scring returns for each Class."""

    def test_project_insert(self, project_object):
        """Test project inster method."""
        assert (
            project_object.insert()
            == """INSERT INTO project (name) VALUES ('Test Project')"""
        )

    def test_project_select_id(self, project_object):
        """Test project select_id method."""
        assert (
            project_object.select_id()
            == """SELECT id FROM project WHERE name='Test Project'"""
        )

    def test_board_instert(self, board_object):
        """Test board inster method."""
        assert (
            board_object.insert()
            == """
            INSERT INTO
                board (project_id, type, name, position)
            VALUES
                (1, 'kanban', 'Test Board 1', 0)
        """
        )

    def test_board_max_position(self, board_object):
        """Test board class method to return required SQL string"""
        assert board_object.max_position() == """SELECT MAX(position) FROM board"""

    def test_board_select_board(self, board_object):
        """Test board select_board method."""
        assert (
            board_object.select_board()
            == """SELECT id, position, project_id FROM board WHERE name='Test Board 1' AND project_id=1"""
        )

    def test_board_select_id(self, board_object):
        """Test board select_id method."""
        assert (
            board_object.select_id()
            == """SELECT id FROM board WHERE name='Test Board 1' AND project_id=1"""
        )

    def test_list_instert(self, list_object):
        """Test list inster method."""
        assert (
            list_object.insert()
            == """
            INSERT INTO
                list (board_id, name, position)
            VALUES
                (1, 'Test List 1', 0)
        """
        )

    def test_list_max_position(self, list_object):
        """Test list class method to return required SQL string"""
        assert list_object.max_position() == """SELECT MAX(position) FROM list"""

    def test_list_select_list(self, list_object):
        """Test list select_list method."""
        assert (
            list_object.select_list()
            == """SELECT id, position, board_id FROM list WHERE name='Test List 1' AND board_id=1"""
        )

    def test_list_select_id(self, list_object):
        """Test list select_id method."""
        assert (
            list_object.select_id()
            == """SELECT id FROM list WHERE name='Test List 1' AND board_id=1"""
        )

    def test_get_tasks(self, card_object):
        """Test card get_tasks method."""
        assert card_object.get_tasks() == """SELECT name FROM task WHERE card_id=1"""

    def test_card_instert(self, card_object):
        """Test card inster method."""
        assert (
            card_object.insert()
            == """
                    INSERT INTO
                        card (board_id, list_id, name, position)
                    VALUES
                        (1, 1, 'Test Card 1', 0)
                """
        )

    def test_card_max_position(self, card_object):
        """Test card class method to return required SQL string"""
        assert card_object.max_position() == """SELECT MAX(position) FROM card"""

    def test_card_select_card(self, card_object):
        """Test card select_card method."""
        assert (
            card_object.select_card()
            == """SELECT id, position, board_id, list_id FROM card WHERE name='Test Card 1' AND board_id=1 AND list_id=1"""
        )

    def test_card_select_id(self, card_object):
        """Test card select_id method."""
        assert (
            card_object.select_id()
            == """SELECT id FROM card WHERE name='Test Card 1' AND board_id=1 AND list_id=1"""
        )
