"""Unittest-based data quality and report generation tool."""
import io
import sys
import unittest
import logging
import argparse
import datetime
from typing import Dict, Callable, Optional, Tuple

import matplotlib
import matplotlib.pyplot as plt
import jinja2
import markdown

# assume that one report will be generated
FIGURES: Dict[str, Dict[str, str]] = dict()
logger = logging.getLogger(__name__)

print("Figures created.")


def clear_figures():
    """Clear global figure dictionary."""
    logger.debug("Going to clear %i figures.", len(FIGURES))
    FIGURES.clear()


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

        print(FIGURES.keys())

    return wrapper


# def discover_and_run(pattern: str = "test*.py", templates_dir: str = "templates"):
#     """Discover unittests and run them, and generate report."""

#     # discover all of the test cases and run them
#     tests = unittest.defaultTestLoader.discover(".", pattern=pattern)
#     import pdb

#     pdb.set_trace()
#     runner = unittest.TextTestRunner()
#     result = runner.run(tests)  # result returns errors, failures, skipped tests
#     if result.errors:  # errors in setup or teardown occurred
#         logger.error(f"Report cannot be generated: errors raised whilst running tests.")
#         sys.exit(1)

#     # NB: figures are empty!

#     # compile into single html from template and style
#     env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_dir))
#     env.filters["markdown"] = markdown.markdown
#     template = env.get_template("index.html")
#     # generate report
#     html = template.render(figures=FIGURES, date=datetime.datetime.now().ctime())
#     # save html
#     with open("report.html", "w") as f:
#         f.write(html)


# if __name__ == "__main__":
#     parser = argparse.ArgumentParser(description=__doc__)
#     parser.add_argument(
#         "--pattern", default="test*.py", help="File patterns to discover test cases in."
#     )
#     parser.add_argument(
#         "--templates_dir",
#         default="templates",
#         help="Path to jinja2 templates directory including index.html and main.css",
#     )
#     args = parser.parse_args()

#     discover_and_run(pattern=args.pattern, templates_dir=args.templates_dir)
