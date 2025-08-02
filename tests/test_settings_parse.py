from scripts.utils.parse_settings import config_to_settings
import tempfile


def test():
    text = """[audio]
device=default

[stt]
engine=whisper

[classifiers]
keywords=alert,security
"""

    tmp = tempfile.NamedTemporaryFile(suffix='.ini', delete=False)
    with open(tmp.name, 'w', encoding='utf8', newline='') as f:
        f.write(text)

    settings = config_to_settings(tmp.name)
    assert settings["audio.device"] == "default"
    assert settings["stt.engine"] == "whisper"
    assert settings["classifiers.keywords"] == "alert,security"
