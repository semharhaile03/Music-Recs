import unittest
import pandas as pd
from tester import view_library
from pandas.testing import assert_frame_equal


class TestViewLibrary(unittest.TestCase):
    def test_library_with_duplicate_songs(self):
        favorites = pd.DataFrame({"Title": ["Song A", "Song B", "Song A"],
                                  "Artist":
                                  ["Artist X", "Artist Y", "Artist X"]})
        expected_result = pd.DataFrame(
            {"Title": ["Song A", "Song B"], "Artist": ["Artist X", "Artist Y"]})
        result = view_library(favorites)
        assert_frame_equal(result, expected_result)
