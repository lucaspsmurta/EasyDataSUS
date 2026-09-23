"""Opt-in, context-local diagnostics for evaluation; no global request history."""
from contextlib import contextmanager
from contextvars import ContextVar

_records = ContextVar('generation_diagnostics', default=None)


def record(stage, **details):
    records = _records.get()
    if records is not None:
        records.append(dict(stage=stage, **details))


@contextmanager
def capture():
    records = []
    token = _records.set(records)
    try:
        yield records
    finally:
        _records.reset(token)
