"""Small sound-effects manager with generated tones and optional WAV overrides."""

import math
import struct
from pathlib import Path

import pygame


class SoundEffects:
    SAMPLE_RATE = 22050
    VOLUME = 0.28

    def __init__(self):
        self.enabled = False
        self.flap_sound = None
        self.score_sound = None
        self.hit_sound = None

        assets_dir = Path(__file__).resolve().parent.parent / "assets"
        try:
            if pygame.mixer.get_init() is None:
                pygame.mixer.init(
                    frequency=self.SAMPLE_RATE,
                    size=-16,
                    channels=1,
                    allowedchanges=0,
                )
            if pygame.mixer.get_init() is None:
                return
            self.enabled = True
            self.flap_sound = self._load_or_generate(
                assets_dir / "flap.wav", 700, 420, 0.09
            )
            self.score_sound = self._load_or_generate(
                assets_dir / "score.wav", 880, 1320, 0.16
            )
            self.hit_sound = self._load_or_generate(
                assets_dir / "hit.wav", 240, 65, 0.28
            )
        except (pygame.error, OSError, RuntimeError):
            # A missing/unavailable audio device must not prevent the game running.
            self.enabled = False
            self.flap_sound = self.score_sound = self.hit_sound = None

    def _load_or_generate(self, path, start_frequency, end_frequency, duration):
        if path.is_file():
            try:
                return pygame.mixer.Sound(str(path))
            except (pygame.error, OSError):
                # Use a generated replacement for this sound only.
                pass

        mixer_info = pygame.mixer.get_init()
        if mixer_info is None:
            return None
        sample_rate, sample_size, channels = mixer_info
        if sample_size != -16:
            return None
        pcm = self._generate_samples(
            sample_rate,
            channels,
            start_frequency,
            end_frequency,
            duration,
            self.VOLUME,
        )
        if not pcm:
            return None
        try:
            return pygame.mixer.Sound(buffer=pcm)
        except pygame.error:
            return None

    @staticmethod
    def _generate_samples(sample_rate, channels, start_frequency, end_frequency, duration, volume):
        if sample_rate <= 0 or channels <= 0 or duration <= 0:
            return b""
        sample_count = max(1, int(sample_rate * duration))
        amplitude = int(32767 * max(0.0, min(volume, 1.0)))
        pcm = bytearray()
        phase = 0.0

        for index in range(sample_count):
            time_seconds = index / sample_rate
            progress = index / max(1, sample_count - 1)
            frequency = start_frequency + (end_frequency - start_frequency) * progress
            phase += 2.0 * math.pi * frequency / sample_rate
            attack = min(1.0, time_seconds / 0.008)
            release = min(1.0, max(0.0, duration - time_seconds) / 0.035)
            envelope = max(0.0, min(attack, release))
            sample = int(amplitude * envelope * math.sin(phase))
            packed_sample = struct.pack("<h", sample)
            for _ in range(channels):
                pcm.extend(packed_sample)
        return bytes(pcm)

    @staticmethod
    def _play(sound):
        if sound is None:
            return
        try:
            sound.play()
        except (pygame.error, RuntimeError):
            # Ignore runtime audio failures; gameplay should continue.
            pass

    def play_flap(self):
        if self.enabled:
            self._play(self.flap_sound)

    def play_score(self):
        if self.enabled:
            self._play(self.score_sound)

    def play_death(self):
        if self.enabled:
            self._play(self.hit_sound)
