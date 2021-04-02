from src.server.token import devFlag
import unittest


class BotTest(unittest.TestCase):
    def setUp(self) -> None:
        self.devFlag = devFlag

    def testFlag(self):
        self.assertFalse(self.devFlag)
