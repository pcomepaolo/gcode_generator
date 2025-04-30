from settings.settings_manager import SettingsManager
import pytest

@pytest.fixture
def settings() -> SettingsManager:
    return SettingsManager()

def test_convert_type(settings: SettingsManager):
    assert type(settings.convert_type('0.3')) is float
    assert type(settings.convert_type('3')) is int
    assert type(settings.convert_type('wer')) is str

def test_value(settings: SettingsManager):
    assert settings.value('filename') is not None

def test_value_failed(settings: SettingsManager):
    with pytest.raises(TypeError):
        settings.value('test')