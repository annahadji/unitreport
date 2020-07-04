import argparse
import jinja2
import unittest
import markdown
import datetime
import sys
import logging

import unitreport

logger = logging.getLogger(__name__)


def discover_and_run(pattern: str = "test*.py", templates_dir: str = "templates"):
    """Discover unittests and run them, and generate report."""

    # discover all of the test cases and run them
    tests = unittest.defaultTestLoader.discover(".", pattern=pattern)
    runner = unittest.TextTestRunner()
    result = runner.run(tests)  # result returns errors, failures, skipped tests
    if result.errors:  # errors in setup or teardown occurred
        logger.error(f"Report cannot be generated: errors raised whilst running tests.")
        sys.exit(1)

    # compile into single html from template and style
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(templates_dir))
    env.filters["markdown"] = markdown.markdown
    template = env.get_template("index.html")
    # generate report
    html = template.render(
        figures=unitreport.FIGURES, date=datetime.datetime.now().ctime()
    )
    # save html
    with open("report.html", "w") as f:
        f.write(html)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pattern", default="test*.py", help="File patterns to discover test cases in."
    )
    parser.add_argument(
        "--templates_dir",
        default="templates",
        help="Path to jinja2 templates directory including index.html and main.css",
    )
    args = parser.parse_args()

    discover_and_run(pattern=args.pattern, templates_dir=args.templates_dir)
