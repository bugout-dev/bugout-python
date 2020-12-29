import argparse
import textwrap

from .app import Bugout


def get_methods_list(args: argparse.Namespace) -> None:
    """
    Return list of all API methods.
    """
    methods = [method for method in Bugout.__dict__.keys()]
    print(methods[2:-3])


def main() -> None:
    bugout_description = textwrap.dedent(
        """\
        Bugout API: Tools for helping with Bugout API.
        """
    )
    parser = argparse.ArgumentParser(prog="bugout", description=bugout_description)
    parser.set_defaults(func=lambda _: parser.print_help())
    subcommands = parser.add_subparsers(description="Bugout API commands")

    parser_common = subcommands.add_parser(
        "methods", description="Work with Bugout users API handlers"
    )
    parser_common.set_defaults(func=get_methods_list)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
