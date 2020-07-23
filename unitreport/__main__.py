"""Main entry point for unitreport."""
import pathlib
import argparse

from . import generate


if __name__ == "__main__":

    parser = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument("--tests_dir", default=".", help="Path to test files.")
    parser.add_argument(
        "--pattern", default="test*.py", help="File patterns to discover test cases in."
    )
    parser.add_argument(
        "--templates_dir",
        default=str(pathlib.Path(__file__).parent / "templates"),
        help="Path to jinja2 templates directory including index.html and main.css.",
    )
    parser.add_argument(
        "--output_file", default="report.html", help="Output path including name.",
    )
    args = parser.parse_args()

    generate.main(
        tests_dir=args.tests_dir,
        pattern=args.pattern,
        templates_dir=args.templates_dir,
        output_file=args.output_file,
    )
