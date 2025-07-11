import pytest
import pandas as pd
from definition_2432b7a0973d4e049d22ac6ba758cfd3 import load_control_data

def test_load_control_data_synthetic():
    df = load_control_data(file_path=None, generate_synthetic=True)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty

def test_load_control_data_file_not_found(tmp_path):
    file_path = tmp_path / "nonexistent_file.csv"
    with pytest.raises(FileNotFoundError):
        load_control_data(file_path=file_path, generate_synthetic=False)

def test_load_control_data_empty_file(tmp_path):
    file_path = tmp_path / "empty_file.csv"
    file_path.write_text("")
    df = load_control_data(file_path=file_path, generate_synthetic=False)
    assert isinstance(df, pd.DataFrame)
    assert df.empty

def test_load_control_data_with_file(tmp_path):
    file_path = tmp_path / "test_file.csv"
    file_path.write_text("col1,col2\n1,2\n3,4")
    df = load_control_data(file_path=file_path, generate_synthetic=False)
    assert isinstance(df, pd.DataFrame)
    assert not df.empty
    assert len(df) == 2

def test_load_control_data_no_file_no_synthetic():
    with pytest.raises(ValueError):
        load_control_data(file_path=None, generate_synthetic=False)
