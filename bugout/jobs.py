"""
This module makes it easy to use a Bugout journal as a job queue. It is inspired by the Bugout Segment
integration: https://github.com/bugout-dev/thorax
"""

from datetime import datetime
import requests
from uuid import UUID

from .app import Bugout
from .data import AuthType, BugoutSearchResult
from .journal import SearchOrder
from .settings import BUGOUT_BROOD_URL, BUGOUT_SPIRE_URL, REQUESTS_TIMEOUT


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
        journal_id: UUID,
        context_type: str = "job",
        success_tag: str = "job:success",
        failure_tag: str = "job:failure",
        cursor_context_type: str = "job_cursor",
        brood_api_url: str = BUGOUT_BROOD_URL,
        spire_api_url: str = BUGOUT_SPIRE_URL,
        write_timeout: float = REQUESTS_TIMEOUT,
        auth_type: AuthType = AuthType.bearer,
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

    def create_job(self, job_id: str, job_title: str, job_content: str) -> None:
        """
        Create a job in the jobs journal.
        """
        self.client.create_entry(
            self.bugout_token,
            self.journal_id,
            job_title,
            job_content,
            context_id=job_id,
            context_type=self.context_type,
            timeout=self.write_timeout,
        )

    def update_cursor(self, created_at: datetime):
        """
        Update the position of the cursor in the journal to the given "created_at" time.

        This is done by simply creating a new entry representing the cursor position.
        """
        cursor_tag = f"cursor:{self.cursor_context_type}"
        headers = {"Authorization": f"{self.auth_type.value} {self.bugout_token}"}
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
    ) -> list[BugoutSearchResult]:
        """
        List all remaining jobs. These are jobs that have neither been marked as complete nor as failed.
        If the use_cursor argument is True, this only returns jobs since the most recent cursor. If it is
        False, remaining_jobs returns all incomplete and unfailed jobs since the beginning of time.

        Jobs are returned in chronological order.
        """
        query_components: list[str] = [
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

        return job_results.results
