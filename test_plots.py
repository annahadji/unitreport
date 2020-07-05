"""Short example use case of generating plots using unitreport library."""
import unittest

import seaborn as sns
import pandas as pd

import unitreport


class TestPlot(unittest.TestCase):
    """An example test suite producing plots to generate a report using unitreport."""

    dataset: pd.DataFrame = None

    @classmethod
    def setUpClass(cls):
        """Load dataset on setup."""
        cls.dataset = sns.load_dataset("fmri")

    @unitreport.plotting
    def test_timepoint_vs_signal_by_event(self):
        """*fMRI data:* timepoint versus signal for stim and cue events."""
        # you can still run assertions to check data quality before plotting
        self.assertEqual(self.dataset.shape, (1064, 5))

        # plotting decorator will call plt.savefig() to generate the plot
        sns.relplot(
            x="timepoint",
            y="signal",
            hue="event",
            style="event",
            kind="line",
            data=self.dataset,
        )

    @unitreport.plotting
    def test_timepoint_vs_signal_by_event_and_region(self):
        """*fMRI data:* timepoint versus signal for events and regions.
        Colour distinguishes region and symbol distinguishes events.
        """
        # you can also return a plot and plotting decorator will call .savefig() on the returned object
        return sns.relplot(
            x="timepoint",
            y="signal",
            hue="region",
            style="event",
            dashes=False,
            markers=True,
            kind="line",
            data=self.dataset,
        )

