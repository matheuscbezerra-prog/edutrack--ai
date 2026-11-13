"""
Script for calculating academic subject progress based on tasks fetched from CRUD endpoints.
"""

import os
import json
import argparse
from pathlib import Path
from typing import Optional, Dict, Any, Union, List
import requests

COMPLETED_STATUSES = {"completed", "concluida", "concluída", "done"}


def get_base_url() -> str:
    """Retrieve base URL for CRUD endpoints from environment variable or .env file."""
    base_url = os.getenv("CRUD_BASE_URL") or os.getenv("BASE_URL")
    if not base_url:
        env_path = Path(__file__).resolve().parent.parent / ".env"
        if env_path.exists():
            try:
                with open(env_path, "r", encoding="utf-8") as file:
                    for line in file:
                        line = line.strip()
                        if line and not line.startswith("#") and "=" in line:
                            key, val = line.split("=", 1)
                            key_clean = key.strip()
                            val_clean = val.strip().strip("'\"").rstrip("/")
                            if key_clean == "CRUD_BASE_URL":
                                return val_clean
                            elif key_clean == "BASE_URL" and not base_url:
                                base_url = val_clean
            except Exception:
                pass

    if base_url:
        clean_url = base_url.strip().rstrip("/")
        # If pointing to the Authentication canonical, adapt to Workspace canonical where CRUD lives
        if clean_url.endswith("/api:rkQbZi0C"):
            return clean_url.replace("/api:rkQbZi0C", "/api:Ue0jQHHF")
        return clean_url

    return "https://x8ki-letl-twmt.n7.xano.io/api:Ue0jQHHF"


def fetch_tasks_for_subject(
    subject_id: int,
    auth_token: Optional[str] = None,
    base_url: Optional[str] = None
) -> List[Dict[str, Any]]:
    """
    Fetch tasks for a given subject using the CRUD GET /academic_tasks endpoint.

    Args:
        subject_id: ID of the subject to fetch tasks for.
        auth_token: Optional Bearer authentication token.
        base_url: Optional base URL override for the CRUD endpoint.

    Returns:
        List of task dictionaries.
    """
    url_base = (base_url or get_base_url()).rstrip("/")
    if url_base.endswith("/api:rkQbZi0C"):
        url_base = url_base.replace("/api:rkQbZi0C", "/api:Ue0jQHHF")

    url = f"{url_base}/academic_tasks"
    params = {"subject_id": subject_id}
    headers = {}
    if auth_token:
        headers["Authorization"] = f"Bearer {auth_token}"

    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()

    data = response.json()
    if isinstance(data, list):
        return data
    return []


def compute_progress_metrics(subject_id: int, tasks: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculate progress statistics from a list of task records.

    Args:
        subject_id: ID of the subject.
        tasks: List of task records.

    Returns:
        Dictionary with subject_id, total_tasks, completed_tasks, pending_tasks,
        and progress_percentage.
    """
    total_tasks = len(tasks)
    completed_tasks = sum(
        1 for task in tasks
        if str(task.get("status", "")).strip().lower() in COMPLETED_STATUSES
    )
    pending_tasks = total_tasks - completed_tasks

    if total_tasks > 0:
        progress_percentage = round((completed_tasks / total_tasks * 100.0), 2)
    else:
        progress_percentage = 0.0

    return {
        "subject_id": subject_id,
        "total_tasks": total_tasks,
        "completed_tasks": completed_tasks,
        "pending_tasks": pending_tasks,
        "progress_percentage": progress_percentage,
    }


def calculate_subject_progress(
    subject_id: int,
    auth_token: Optional[str] = None,
    base_url: Optional[str] = None,
    as_json_string: bool = True
) -> Union[str, Dict[str, Any]]:
    """
    Calculate progress percentage for a subject based on its tasks fetched from CRUD endpoints.

    Args:
        subject_id: ID of the academic subject.
        auth_token: Optional Bearer token for authenticated access.
        base_url: Optional base URL for the API endpoint.
        as_json_string: Whether to return a formatted JSON string or dictionary.

    Returns:
        JSON string or dictionary containing progress metrics.
    """
    try:
        tasks = fetch_tasks_for_subject(subject_id, auth_token=auth_token, base_url=base_url)
        result = compute_progress_metrics(subject_id, tasks)
    except requests.exceptions.RequestException as error:
        result = {
            "subject_id": subject_id,
            "error": f"Network/API error fetching tasks: {error}",
            "total_tasks": 0,
            "completed_tasks": 0,
            "pending_tasks": 0,
            "progress_percentage": 0.0,
        }
    except Exception as error:
        result = {
            "subject_id": subject_id,
            "error": f"Unexpected error calculating progress: {error}",
            "total_tasks": 0,
            "completed_tasks": 0,
            "pending_tasks": 0,
            "progress_percentage": 0.0,
        }

    if as_json_string:
        return json.dumps(result, indent=2, ensure_ascii=False)
    return result


def main():
    """Command-line entrypoint for calculate_progress.py."""
    parser = argparse.ArgumentParser(
        description="Calculate subject progress percentage from academic tasks CRUD API."
    )
    parser.add_argument("--subject-id", type=int, required=True, help="ID of the subject")
    parser.add_argument("--token", type=str, default=None, help="Optional user auth token")
    parser.add_argument("--base-url", type=str, default=None, help="Optional CRUD API base URL")

    args = parser.parse_args()

    output = calculate_subject_progress(
        subject_id=args.subject_id,
        auth_token=args.token,
        base_url=args.base_url,
        as_json_string=True,
    )
    print(output)


if __name__ == "__main__":
    main()
