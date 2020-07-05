"""Short example use case of generating tables using unitreport library."""
import unittest

import seaborn as sns
import pandas as pd

import unitreport


class TestTable(unittest.TestCase):
    """An example test suite returning tables to generate a report using unitreport."""

    dataset: pd.DataFrame = None

    @classmethod
    def setUpClass(cls):
        """Load dataset on setup."""
        cls.dataset = sns.load_dataset("fmri")

    @unitreport.tabling
    def test_region_counts(self):
        """*fMRI data:* table summary description of timepoints and signals."""
        # you can still run assertions to check data quality before making table
        self.assertEqual(self.dataset.shape, (1064, 5))

        return self.dataset.describe().to_html()
