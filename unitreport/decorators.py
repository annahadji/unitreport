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
        func:
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
