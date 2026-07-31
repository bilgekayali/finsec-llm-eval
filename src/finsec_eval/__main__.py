"""Allow ``python -m finsec_eval`` to run the command-line interface."""

from finsec_eval.cli import entrypoint


if __name__ == "__main__":
    entrypoint()
