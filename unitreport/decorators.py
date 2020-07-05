"""Decorators and global figures for unittest-based data quality and report generation tool."""
import io
import unittest
import logging
from typing import Dict, Callable, Optional, Tuple

import matplotlib
import matplotlib.pyplot as plt


# assume that one report will be generated
FIGURES: Dict[str, Dict[str, str]] = dict()
logger = logging.getLogger(__name__)


def plotting(
    func: Callable[..., Optional[matplotlib.figure.Figure]],
    figsize: Tuple[float, float] = (8, 6),
):
    """Decorator for tests that generate matplotlib figures.

    Args:
        func: function passed to decorator
        figsize: [description]. Defaults to (8, 6).
    """

    def wrapper(*args, **kwargs):
        # create clean figure for test case to utilise
        plt.figure(figsize=figsize)
        # call test case, if fails will raise error and rest of plot saving will not run
        fig = func(*args, **kwargs) or plt
        # save plot and description to buffer
        buffer = io.StringIO()
        fig.savefig(buffer, format="svg", bbox_inches="tight")
        FIGURES[func.__name__] = {
            "type": "plot",
            "content": buffer.getvalue(),
            "description": func.__doc__ or "",
        }
        logger.debug(
            "Ran %s with buffer size %i.", func.__name__, len(buffer.getvalue())
        )

    return wrapper


def tabling(func: Callable[..., str]):
    """Decorator for tests that return (html) tables

    Args:
        func: function passed to decorator
    """

    def wrapper(*args, **kwargs):
        # call test case, if fails will raise error and table wont be saved
        html_table = func(*args, **kwargs)
        # save table and description to buffer
        FIGURES[func.__name__] = {
            "type": "table",
            "content": html_table,
            "description": func.__doc__ or "",
        }
        logger.debug(
            "Ran %s with html string length %i", func.__name__, len(html_table)
        )

    return wrapper
