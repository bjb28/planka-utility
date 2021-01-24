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
