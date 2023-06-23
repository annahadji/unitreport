"""Decorators and global figures for unittest-based data quality and report generation tool."""
import io
import unittest
import logging
from typing import Dict, Callable, Optional, Tuple, TypeVar

import matplotlib

# render matplotlib figures to file, not to window
matplotlib.use("Agg")
import matplotlib.pyplot as plt


# assume that one report will be generated
FIGURES: Dict[str, Dict[str, str]] = dict()
logger = logging.getLogger(__name__)

# type which matches any subclass of unittest.TestCase
TestCaseType = TypeVar("TestCaseType", bound=unittest.TestCase)


def plotting(
    figsize: Tuple[float, float] = (8, 6),
    dpi: int = 100,
    save_to_disk: bool = False,
):
    """Decorator for tests that generate matplotlib figures.

    Args:
        figsize: (plt) figure size. Defaults to (8, 6).
        dpi: (plt) figure dpi. Defaults to 100.
        save_to_disk: save figure separately to disk. Defaults to False.
    """

    def plotting_decorator(
        func: Callable[[TestCaseType], Optional[matplotlib.figure.Figure]]
    ):
        def wrapper(testcase: TestCaseType):
            # create clean figure for test case to utilise
            plt.figure(figsize=figsize, dpi=dpi)
            # call test case, if fails will raise error and rest of plot saving will not run
            fig = func(testcase) or plt
            # save to in-memory buffer to avoid writing to file
            buffer = io.StringIO()
            fig.savefig(buffer, format="svg", bbox_inches="tight")
            if save_to_disk:
                fig.savefig(
                    f"{func.__name__}.png", transparent=True, bbox_inches="tight"
                )
            # dont include empty plot in report
            testcase.assertTrue(
                len(buffer.getvalue()), "Generated plot with empty output."
            )
            # if above assertion fails, following code will not be run
            FIGURES[func.__name__] = {
                "type": "plot",
                "content": buffer.getvalue(),
                "description": func.__doc__ or "",
            }
            logger.debug(
                "Ran %s with buffer size %i.", func.__name__, len(buffer.getvalue())
            )

        return wrapper

    return plotting_decorator


def tabling(func: Callable[[TestCaseType], str]):
    """Decorator for tests that return (html) tables

    Args:
        func: function passed to decorator.
    """

    def wrapper(testcase: TestCaseType):
        # call test case, if fails will raise error and table wont be saved
        html_table = func(testcase)
        # dont include empty table in report
        testcase.assertIsInstance(html_table, str, "Returned table is not a string.")
        testcase.assertTrue(len(html_table), "Returned table is empty.")
        FIGURES[func.__name__] = {
            "type": "table",
            "content": html_table,
            "description": func.__doc__ or "",
        }
        logger.debug(
            "Ran %s with html string length %i", func.__name__, len(html_table)
        )

    return wrapper
