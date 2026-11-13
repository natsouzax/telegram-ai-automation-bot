import tempfile
import unittest
from pathlib import Path

from storage import SubscriberStore


class SubscriberStoreTests(unittest.TestCase):
    def test_subscribe_and_delete(self):
        with tempfile.TemporaryDirectory() as directory:
            store = SubscriberStore(str(Path(directory) / "test.db"))
            store.subscribe(123)
            self.assertEqual(
                store.conn.execute("SELECT telegram_id FROM subscribers").fetchall(),
                [(123,)],
            )
            store.unsubscribe(123)
            self.assertEqual(
                store.conn.execute("SELECT telegram_id FROM subscribers").fetchall(),
                [],
            )
            store.close()


if __name__ == "__main__":
    unittest.main()
