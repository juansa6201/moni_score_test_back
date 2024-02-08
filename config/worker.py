from __future__ import annotations

from uvicorn.workers import UvicornWorker


class ScoringUvicornWorker(UvicornWorker):
    CONFIG_KWARGS = {'loop': 'auto', 'http': 'auto', 'server_header': False}
