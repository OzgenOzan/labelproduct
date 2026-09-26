"""Tests for the labelling logic in labelbyapi.py (LP-1, LP-3).

The script keeps its labelling logic at module level (it reads/writes Excel
files on import), so it is loaded via importlib with pandas Excel I/O
monkeypatched to operate on a small in-memory DataFrame.

The sibling script "labelbyapi andmanufacturer.py" duplicates this logic
(~85%, LP-2) and cannot be imported by module name due to the space in its
file name; it is covered only indirectly here. See the remediation PR for
the residual-duplication note.
"""
import importlib.util
from pathlib import Path

import numpy as np
import pandas as pd

REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT_PATH = REPO_ROOT / "labelbyapi.py"
MISSING_KEY = "<MISSING>"


def run_labelbyapi(monkeypatch, df):
    """Execute labelbyapi.py with Excel I/O replaced by in-memory fakes.

    Returns (module, output_df)."""
    saved = {}

    def fake_read_excel(*args, **kwargs):
        return df.copy()

    def fake_to_excel(self, *args, **kwargs):
        saved["df"] = self

    monkeypatch.setattr(pd, "read_excel", fake_read_excel)
    monkeypatch.setattr(pd.DataFrame, "to_excel", fake_to_excel)

    spec = importlib.util.spec_from_file_location("labelbyapi_under_test", SCRIPT_PATH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module, saved["df"]


def test_normal_labelling_assigns_sequential_codes(monkeypatch):
    df = pd.DataFrame({"Active Ingredient": ["paracetamol", "Ibuprofen ", "ASPIRIN"]})
    module, out = run_labelbyapi(monkeypatch, df)
    assert out["Product Code"].tolist() == [0, 1, 2]
    # Keys are normalized (stripped + uppercased)
    assert set(module.code_map) == {"PARACETAMOL", "IBUPROFEN", "ASPIRIN"}


def test_nan_key_maps_to_sentinel_consistently(monkeypatch):
    df = pd.DataFrame({"Active Ingredient": [np.nan, " aspirin ", np.nan]})
    module, out = run_labelbyapi(monkeypatch, df)
    # Both NaN rows must share ONE deterministic code via the sentinel (LP-1)
    assert MISSING_KEY in module.code_map
    assert out["Product Code"].tolist() == [0, 1, 0]


def test_duplicate_keys_get_same_code(monkeypatch):
    df = pd.DataFrame({"Active Ingredient": ["Aspirin", "ASPIRIN", "aspirin ", "other"]})
    module, out = run_labelbyapi(monkeypatch, df)
    assert out["Product Code"].tolist() == [0, 0, 0, 1]


def test_dict_builtin_not_shadowed(monkeypatch):
    df = pd.DataFrame({"Active Ingredient": ["x"]})
    module, _ = run_labelbyapi(monkeypatch, df)
    assert not hasattr(module, "dict")  # LP-3: variable renamed to code_map
    assert isinstance(module.code_map, dict)
