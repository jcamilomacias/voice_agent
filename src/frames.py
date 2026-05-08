from dataclasses import dataclass


@dataclass
class Frame:
    pass


@dataclass
class StartFrame(Frame):
    pass


@dataclass
class EndFrame(Frame):
    pass


@dataclass
class AudioRawFrame(Frame):
    audio: bytes
    sample_rate: int
    num_channels: int

    def __post_init__(self):
        if not isinstance(self.audio, bytes):
            raise TypeError(f"audio must be bytes, got {type(self.audio)}")
        if not isinstance(self.sample_rate, int):
            raise TypeError(f"sample_rate must be int, got {type(self.sample_rate)}")
        if not isinstance(self.num_channels, int):
            raise TypeError(f"num_channels must be int, got {type(self.num_channels)}")
