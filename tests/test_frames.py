import pytest
from src.frames import AudioRawFrame, StartFrame, EndFrame


def test_audio_raw_frame_instantiates():
    frame = AudioRawFrame(audio=b"\x00\x01", sample_rate=16000, num_channels=1)
    assert frame.audio == b"\x00\x01"
    assert frame.sample_rate == 16000
    assert frame.num_channels == 1


def test_start_frame_instantiates():
    frame = StartFrame()
    assert isinstance(frame, StartFrame)


def test_end_frame_instantiates():
    frame = EndFrame()
    assert isinstance(frame, EndFrame)


def test_audio_raw_frame_wrong_type_raises():
    with pytest.raises((TypeError, Exception)):
        AudioRawFrame(audio="not bytes", sample_rate=16000, num_channels=1)
