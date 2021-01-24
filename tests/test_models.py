#!/usr/bin/env pytest -vs
"""Tests for Models."""

# Custom Libraries
from models.models import Board, Card, List, Project


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
