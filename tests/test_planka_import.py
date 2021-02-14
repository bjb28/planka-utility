#!/usr/bin/env pytest -vs
"""Tests for Models."""
# Standard imports
import json
import os

# Custom Libraries
from tools.planka_import import generate_template


class TestTemplate:
    """Test the template method"""

    def test_generate_template(self, tmp_path, template_json):
        """Test Generate Template method"""
        os.chdir(tmp_path)
        generate_template()
        with open("planka_template.json", "r") as fp:
            output = json.load(fp)

        assert output == template_json
