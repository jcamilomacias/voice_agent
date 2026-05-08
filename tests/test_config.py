import os
import pytest
from unittest.mock import patch


def test_sample_rate_default():
    with patch.dict(os.environ, {}, clear=False):
        os.environ.pop("SAMPLE_RATE", None)
        # Re-import to get fresh settings
        import importlib
        import src.config as cfg
        importlib.reload(cfg)
        settings = cfg.Settings()
        assert settings.sample_rate == 16000


def test_sample_rate_from_env():
    with patch.dict(os.environ, {"SAMPLE_RATE": "8000"}):
        import importlib
        import src.config as cfg
        importlib.reload(cfg)
        settings = cfg.Settings()
        assert settings.sample_rate == 8000


def test_chunk_size_default():
    with patch.dict(os.environ, {}, clear=False):
        os.environ.pop("CHUNK_SIZE", None)
        import importlib
        import src.config as cfg
        importlib.reload(cfg)
        settings = cfg.Settings()
        assert settings.chunk_size == 512


def test_chunk_size_from_env():
    with patch.dict(os.environ, {"CHUNK_SIZE": "1024"}):
        import importlib
        import src.config as cfg
        importlib.reload(cfg)
        settings = cfg.Settings()
        assert settings.chunk_size == 1024
