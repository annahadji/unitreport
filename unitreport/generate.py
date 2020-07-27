"""Test orchestration and report generation module."""
import pathlib
import datetime
import logging
import unittest
from typing import Dict, Tuple

import jinja2
import markdown

from .decorators import FIGURES

logger = logging.getLogger(__name__)


def discover_and_run(
    tests_dir: str = ".", pattern: str = "test*.py",
) -> Tuple[unittest.TestResult, Dict[str, Dict[str, str]]]:
    """Discover unittests and run them.

    Args:
        tests_dir (str, optional): Path to test files. Defaults to ".".
        pattern (str, optional): [description]. Defaults to "test*.py".

    Returns:
        Tuple[unittest.TestResult, Dict[str, Dict[str, str]]]: Result of tests (returns errors,
            failures, skipped tests), global FIGURES dictionary generated from tests.
    """
    # discover all of the test cases and run them
    tests = unittest.defaultTestLoader.discover(tests_dir, pattern=pattern)
    runner = unittest.TextTestRunner()
    result = runner.run(tests)  # result returns errors, failures, skipped tests
    logger.debug("Ran %i tests", result.testsRun)
    return (result, FIGURES)


def generate_report(
    templates_dir: str = str(pathlib.Path(__file__).parent / "templates"),
    output_file: str = "report.html",
    figures: Dict[str, Dict[str, str]] = None,
) -> str:
    """Generate html report, and optionally write to output file if specified.

    Args:
        templates_dir (str, optional): Path to jinja2 templates directory including
            index.html and main.css. Defaults to unitreport "templates".
        output_file (str, optional): Output path including name. Defaults to "report.html".
        figures (Dict[str, Dict[str, str]], optional): Dictionary of figures passed to
            template. Defaults to global FIGURES object.

    Returns:
        str: Generated html report.
    """
    # compile into single html from template and style
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_dir))
    env.filters["markdown"] = markdown.markdown
    template = env.get_template("index.html")
    html = template.render(
        figures=figures or FIGURES, date=datetime.datetime.now().ctime()
    )
    logger.debug("Generated html of length %i", len(html))
    if output_file:
        with open(output_file, "w") as outf:
            outf.write(html)
        logger.info("Saved generated report to %s", output_file)
    return html


def main(
    tests_dir: str = ".",
    pattern: str = "test*.py",
    templates_dir: str = str(pathlib.Path(__file__).parent / "templates"),
    output_file: str = "report.html",
) -> Tuple[unittest.TestResult, Dict[str, Dict[str, str]], str]:
    """Discovers and runs test cases followed by generating the report.

    Args:
        tests_dir (str, optional): Path to test files. Defaults to ".".
        pattern (str, optional): File patterns to discover test cases in. Defaults to "test*.py".
        templates_dir (str, optional): Path to jinja2 templates directory including
            index.html and main.css. Defaults to unitreport "templates").
        output_file (str, optional): Output path including name. Defaults to "report.html".

    Returns:
        Tuple[unittest.TestResult, Dict[str, Dict[str, str]], str]: Test results, global FIGURES
            dictionary generated from tests and generated html report.
    """
    result, figs = discover_and_run(tests_dir=tests_dir, pattern=pattern)
    assert (
        result.testsRun and not result.errors
    ), "Report cannot be generated: errors raised whilst running tests or no tests ran."
    html = generate_report(templates_dir=templates_dir, output_file=output_file)
    return (result, figs, html)
