"""This module provides a CLI tool for creating a structured directory with files for meetings.

The tool generates the following structure based on the current date and time:

docs/
    meetings/
        YYYYMMDD-HHMM/
            00_CONTEXT.md
            01_SESSIONS.md
            02_PROGRESS.md
            03_DECISIONS.md

Usage:
    python script/dev_tools.py meeting
"""

from datetime import datetime
import os

import click


@click.group()
def cli():
    """A CLI tool for creating structured directories for meetings."""
    pass


@cli.command()
def meeting():
    """Creates the directory structure for the current date and time.

    Structure:
    docs/
        meetings/
            YYYYMMDD-HHMM/
                00_CONTEXT.md
                01_SESSIONS.md
                02_PROGRESS.md
                03_DECISIONS.md
    """
    # Get the current date and time
    now = datetime.now()
    timestamp = now.strftime("%Y%m%d-%H%M")

    # Define the base path and target directory
    base_path = os.path.join("docs", "meetings")
    target_dir = os.path.join(base_path, timestamp)

    # List of files to create
    files = [
        "00_CONTEXT.md",
        "01_SESSIONS.md",
        "02_PROGRESS.md",
        "03_DECISIONS.md",
    ]

    try:
        # Create the directory if it doesn't exist
        os.makedirs(target_dir, exist_ok=True)

        # Create each file in the directory
        for file_name in files:
            file_path = os.path.join(target_dir, file_name)
            with open(file_path, "w") as file:
                file.write(f"# {file_name}\n\n")  # Add a placeholder header

        click.echo(f"Structure created successfully at {target_dir}")
    except Exception as e:
        click.echo(f"Error: {e}")


if __name__ == "__main__":
    cli()
