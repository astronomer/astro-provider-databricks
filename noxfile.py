"""Nox automation definitions."""
import os
from pathlib import Path

import nox

nox.options.sessions = ["dev"]
nox.options.error_on_external_run = False
# nox.options.reuse_existing_virtualenvs = True


@nox.session(python="3.10")
def dev(session: nox.Session) -> None:
    """Create a dev environment with everything installed.

    This is useful for setting up IDE for autocompletion etc. Point the
    development environment to ``.nox/dev``.
    """
    session.install("nox")
    session.install("-e", ".[tests]")


def _expand_env_vars(file_path: Path):
    """Expand environment variables in the given file."""
    with file_path.open() as fp:
        yaml_with_env = os.path.expandvars(fp.read())
    with file_path.open("w") as fp:
        fp.write(yaml_with_env)


@nox.session(python=["3.8", "3.9", "3.10"])
@nox.parametrize("airflow", ["2.3", "2.4", "2.5", "2.6", "2.7", "2.8"])
def test(session: nox.Session, airflow) -> None:
    """Run both unit and integration tests."""
    env = {
        "AIRFLOW_HOME": f"~/airflow-{airflow}-python-{session.python}",
        "AIRFLOW__CORE__ALLOWED_DESERIALIZATION_CLASSES": "airflow\\.* astro\\.* astro_databricks\\.*",
    }

    session.install(
        f"apache-airflow[databricks]=={airflow}",
        "--constraint",
        f"https://raw.githubusercontent.com/apache/airflow/constraints-{airflow}.0/constraints-{session.python}.txt",
    )
    session.install("-e", ".[tests]")

    # Log all the installed dependencies
    session.log("Installed Dependencies:")
    session.run("pip3", "freeze")

    test_connections_file = Path("test-connections.yaml")
    if test_connections_file.exists():
        _expand_env_vars(test_connections_file)

    session.run("airflow", "db", "init", env=env)

    # Since pytest is not installed in the nox session directly, we need to set `external=true`.
    session.run(
        "pytest",
        "-vv",
        *session.posargs,
        env=env,
        external=True,
    )


@nox.session(python=["3.8"])
def type_check(session: nox.Session) -> None:
    """Run MyPy checks."""
    session.install("-e", ".[tests]")
    session.run("mypy", "--version")
    session.run("mypy", "src")


@nox.session(python="3.9")
def build_docs(session: nox.Session) -> None:
    """Build release artifacts."""
    session.install("-e", ".[docs]")
    session.chdir("./docs")
    session.run("make", "html")
