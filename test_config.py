import os
import unittest
from unittest.mock import patch
from app.config import Settings

class SettingsTests(unittest.TestCase):
    def test_missing_token_is_rejected(self):
        with patch.dict(os.environ, {"DISCORD_TOKEN": ""}, clear=True):
            with self.assertRaises(ValueError):
                Settings.load().validate()

    def test_valid_token_is_accepted(self):
        with patch.dict(os.environ, {"DISCORD_TOKEN": "test-token"}, clear=True):
            Settings.load().validate()

if __name__ == "__main__":
    unittest.main()
