import argparse
import logging
import textwrap

from .app import Bugout

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def user_get_handler(args: argparse.Namespace) -> None:
    """
    Handler for "users get" subcommand.
    """
    bugout = Bugout(brood_api_url=args.brood_url, spire_api_url=args.spire_url)
    result = bugout.get_user(token=args.token)
    print(result.json())


def main() -> None:
    bugout_description = textwrap.dedent(
        """\
        Bugout API: Tools for helping with Bugout API.
        """
    )
    parser = argparse.ArgumentParser(prog="bugout", description=bugout_description)
    parser.set_defaults(func=lambda _: parser.print_help())
    subcommands = parser.add_subparsers(description="Journal commands")

    parser.add_argument(
        "--brood_url",
        default="http://localhost",
        help="Brood url",
    )
    parser.add_argument(
        "--spire_url",
        default="http://localhost",
        help="Spire url",
    )

    # Users handlers
    parser_users = subcommands.add_parser(
        "user", description="Work with Bugout users API handlers"
    )
    parser_users.set_defaults(
        func=lambda _: parser_users.print_help(), subparser="users"
    )
    subcommands_users = parser_users.add_subparsers(description="Users commands")

    parser_user_get = subcommands_users.add_parser("get", description="Get user")
    parser_user_get.set_defaults(subcommand="get")
    parser_user_get.add_argument(
        "-t",
        "--token",
        required=True,
        help="User token",
    )
    parser_user_get.set_defaults(func=user_get_handler)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
