"""
This module makes it easy to use a Bugout journal as a job queue. It is inspired by the Bugout Segment
integration: https://github.com/bugout-dev/thorax
"""

import argparse
from datetime import datetime
import json
import os
import requests
from typing import Callable, Optional, List

from .app import Bugout
from .data import AuthType, BugoutSearchResultWithEntryID
from .journal import SearchOrder
from .settings import BUGOUT_BROOD_URL, BUGOUT_SPIRE_URL, REQUESTS_TIMEOUT


DEFAULT_CONTEXT_TYPE = "job"
DEFAULT_SUCCESS_TAG = "job:success"
DEFAULT_FAILURE_TAG = "job:failure"
DEFAULT_CURSOR_CONTEXT_TYPE = "job_cursor"


class BugoutJobQueue:
    """
    This class implements a job queue in a Bugout journal.

    This job queue uses:
    1. context_type to represent jobs in the queue.
    2. context_id to represent the id of each job. Bugout journals do not allow duplication of (context_type, context_id),
    so this allows for deduplcation of jobs by context_id.
    3. A special tag that is used to denote whether a job has been completed successfully.
    4. A special tag that is used to denote whether a job failed.
    5. A context_type for entries that represent cursor entries for the job queue.
    """

    def __init__(
        self,
        bugout_token: str,
        journal_id: str,
        context_type: str = DEFAULT_CONTEXT_TYPE,
        success_tag: str = DEFAULT_SUCCESS_TAG,
        failure_tag: str = DEFAULT_FAILURE_TAG,
        cursor_context_type: str = DEFAULT_CURSOR_CONTEXT_TYPE,
        brood_api_url: str = BUGOUT_BROOD_URL,
        spire_api_url: str = BUGOUT_SPIRE_URL,
        write_timeout: float = REQUESTS_TIMEOUT,
        auth_type: str = AuthType.bearer.name,
    ) -> None:
        self.bugout_token = bugout_token
        self.journal_id = journal_id
        self.context_type = context_type
        self.success_tag = success_tag
        self.failure_tag = failure_tag
        self.cursor_context_type = cursor_context_type
        self.client = Bugout(brood_api_url, spire_api_url)
        self.write_timeout = write_timeout
        self.auth_type = auth_type

    def create_job(self, context_id: str, job_title: str, job_content: str) -> None:
        """
        Create a job in the jobs journal.
        """
        self.client.create_entry(
            self.bugout_token,
            self.journal_id,
            job_title,
            job_content,
            tags=[self.context_type, f"{self.context_type}:{context_id}"],
            context_id=context_id,
            context_type=self.context_type,
            timeout=self.write_timeout,
        )

    def update_cursor(self, created_at: datetime):
        """
        Update the position of the cursor in the journal to the given "created_at" time.

        This is done by simply creating a new entry representing the cursor position.
        """
        cursor_tag = f"cursor:{self.cursor_context_type}"
        headers = {"Authorization": f"{self.auth_type} {self.bugout_token}"}
        body = {
            "title": cursor_tag,
            "content": "",
            "tags": [cursor_tag],
            "context_type": self.cursor_context_type,
            "created_at": created_at.isoformat(),
        }
        requests.post(
            self.client.spire_api_url,
            headers=headers,
            json=body,
            timeout=self.write_timeout,
        )

    def remaining_jobs(
        self,
        use_cursor: bool = True,
        limit: int = 10,
        offset: int = 0,
    ) -> List[BugoutSearchResultWithEntryID]:
        """
        List all remaining jobs. These are jobs that have neither been marked as complete nor as failed.
        If the use_cursor argument is True, this only returns jobs since the most recent cursor. If it is
        False, remaining_jobs returns all incomplete and unfailed jobs since the beginning of time.

        Jobs are returned in chronological order.
        """
        query_components: List[str] = [
            f"context_type:{self.context_type}",
            f"!tag:{self.success_tag}",
            f"!tag:{self.failure_tag}",
        ]
        if use_cursor:
            cursor_results = self.client.search(
                self.bugout_token,
                self.journal_id,
                f"context_type:{self.cursor_context_type}",
                limit=1,
                content=False,
                order=SearchOrder.DESCENDING,
                auth_type=self.auth_type,
            )
            if cursor_results.results:
                cursor = cursor_results.results[0]

            created_at = cursor.created_at.replace(" ", "T")
            query_components.append(f"created_at:>{created_at}")

        query = " ".join(query_components)
        job_results = self.client.search(
            self.bugout_token,
            self.journal_id,
            query,
            limit=limit,
            offset=offset,
            content=True,
            order=SearchOrder.ASCENDING,
            auth_type=self.auth_type,
        )

        results = [
            BugoutSearchResultWithEntryID(
                **dict(raw_result), id=raw_result.entry_url.split("/")[-1]
            )
            for raw_result in job_results.results
        ]
        return results

    def job_complete(self, job_id: str) -> None:
        self.client.update_tags(
            self.bugout_token,
            self.journal_id,
            job_id,
            tags=[self.success_tag],
            timeout=self.write_timeout,
            auth_type=self.auth_type,
        )

    def job_failed(self, job_id: str) -> None:
        self.client.update_tags(
            self.bugout_token,
            self.journal_id,
            job_id,
            tags=[self.failure_tag],
            timeout=self.write_timeout,
            auth_type=self.auth_type,
        )


def value_or_environment_variable(
    environment_variable: str, error_if_none: bool
) -> Callable[[Optional[str]], Optional[str]]:
    def type_fn(raw: Optional[str]) -> Optional[str]:
        final = raw
        if not raw:
            final = os.environ.get(environment_variable)

        if not final and error_if_none:
            raise ValueError(f"{environment_variable} not set")

        return final

    return type_fn


def add_queue_args(parser: argparse.ArgumentParser) -> None:
    """
    Mutates the given argument parser by adding common arguments needed to instantiate a job queue for
    all commands in the jobs CLI.
    """
    parser.add_argument(
        "-t",
        "--token",
        required=False,
        default="",
        type=value_or_environment_variable("BUGOUT_JOBS_ACCESS_TOKEN", True),
        help="An access token for the Bugout API. If this is not provided, the BUGOUT_JOBS_ACCESS_TOKEN environment variable is used.",
    )
    parser.add_argument(
        "-j",
        "--journal",
        required=False,
        default="",
        type=value_or_environment_variable("BUGOUT_JOBS_JOURNAL_ID", True),
        help="An access token for the Bugout API. If this is not provided, the BUGOUT_JOBS_JOURNAL_ID environment variable is used.",
    )
    parser.add_argument(
        "--context-type",
        required=False,
        default=DEFAULT_CONTEXT_TYPE,
        help="Context type by which to identify jobs in the journal.",
    )
    parser.add_argument(
        "--success-tag",
        required=False,
        default=DEFAULT_SUCCESS_TAG,
        help="Success tag to attach to successfully completed jobs in the journal.",
    )
    parser.add_argument(
        "--failure-tag",
        required=False,
        default=DEFAULT_FAILURE_TAG,
        help="Failure tag to attach to unsuccessful jobs in the journal.",
    )
    parser.add_argument(
        "--cursor-context-type",
        required=False,
        default=DEFAULT_CURSOR_CONTEXT_TYPE,
        help="Context type by which to identify the cursor in the journal.",
    )
    parser.add_argument(
        "--brood-api-url",
        required=False,
        default=BUGOUT_BROOD_URL,
        help="Brood API URI.",
    )
    parser.add_argument(
        "--spire-api-url",
        required=False,
        default=BUGOUT_SPIRE_URL,
        help="Spire API URI.",
    )
    parser.add_argument(
        "--write-timeout",
        required=False,
        type=float,
        default=30.0,
        help="Timeout for writing jobs and cursors to the job journal.",
    )
    parser.add_argument(
        "--auth-type",
        required=False,
        type=str,
        default=AuthType.bearer.name,
        choices=[AuthType.bearer.name, AuthType.web3.name],
        help="Type of token that you are using to authenticate to the job journal.",
    )


def queue_from_args(args: argparse.Namespace) -> BugoutJobQueue:
    return BugoutJobQueue(
        args.token,
        args.journal,
        args.context_type,
        args.success_tag,
        args.failure_tag,
        args.cursor_context_type,
        args.brood_api_url,
        args.spire_api_url,
        args.write_timeout,
        args.auth_type,
    )


def handle_create_job(args: argparse.Namespace) -> None:
    queue = queue_from_args(args)
    if args.title is None:
        args.title = f"Job ID: {args.id}"
    queue.create_job(args.id, args.title, args.content)


def handle_remaining_jobs(args: argparse.Namespace) -> None:
    queue = queue_from_args(args)
    remaining_jobs = queue.remaining_jobs(args.use_cursor, args.limit, args.offset)
    print(json.dumps([json.loads(job.json()) for job in remaining_jobs]))


def handle_complete_job(args: argparse.Namespace) -> None:
    queue = queue_from_args(args)
    queue.job_complete(args.job_id)


def handle_fail_job(args: argparse.Namespace) -> None:
    queue = queue_from_args(args)
    queue.job_failed(args.job_id)


def generate_cli() -> argparse.ArgumentParser:
    """
    Generates the "bugout-py jobs" CLI.
    """
    parser = argparse.ArgumentParser(
        description="bugout-py jobs: A command-line tool to manage jobs using a Bugout journal"
    )
    parser.set_defaults(func=lambda _: parser.print_help())

    subparsers = parser.add_subparsers()

    create_job_parser = subparsers.add_parser("create-job", help="Create a job")
    add_queue_args(create_job_parser)
    create_job_parser.add_argument("--id", required=True, help="ID for job.")
    create_job_parser.add_argument(
        "--title",
        required=False,
        default=None,
        help="Title for job. If not provided, title is constructed from job ID.",
    )
    create_job_parser.add_argument(
        "--content", required=True, help="Job specification."
    )
    create_job_parser.set_defaults(func=handle_create_job)

    remaining_jobs_parser = subparsers.add_parser(
        "remaining-jobs", help="View remaining jobs in queue (FIFO order)"
    )
    add_queue_args(remaining_jobs_parser)
    remaining_jobs_parser.add_argument(
        "-c",
        "--use-cursor",
        action="store_true",
        help="Set this flag if you want to only view remaining jobs created after the most recent cursor position",
    )
    remaining_jobs_parser.add_argument(
        "--limit", type=int, default=10, help="Number of remaining jobs to view"
    )
    remaining_jobs_parser.add_argument(
        "--offset",
        type=int,
        default=0,
        help="Offset from which to page through remaining jobs",
    )
    remaining_jobs_parser.set_defaults(func=handle_remaining_jobs)

    complete_job_parser = subparsers.add_parser(
        "complete-job", help="Mark a job as complete"
    )
    add_queue_args(complete_job_parser)
    complete_job_parser.add_argument(
        "-i", "--job-id", required=True, help="ID of job to mark as complete."
    )
    complete_job_parser.set_defaults(func=handle_complete_job)

    fail_job_parser = subparsers.add_parser("fail-job", help="Mark a job as failed")
    add_queue_args(fail_job_parser)
    fail_job_parser.add_argument(
        "-i", "--job-id", required=True, help="ID of job to mark as failed."
    )
    fail_job_parser.set_defaults(func=handle_fail_job)

    return parser


def main() -> None:
    parser = generate_cli()
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
