"""Live transcription test against CMU's reference recording (goforward.raw,
16kHz 16-bit mono, a human saying "go forward ten meters")."""
import unittest
from os.path import dirname, join

import speech_recognition as sr

from ovos_stt_plugin_pocketsphinx import PocketSphinxSTTPlugin

AUDIO = join(dirname(__file__), "goforward.raw")


class TestTranscription(unittest.TestCase):
    def test_transcribes_reference_audio(self):
        plugin = PocketSphinxSTTPlugin(config={"lang": "en-us"})
        with open(AUDIO, "rb") as f:
            audio = sr.AudioData(f.read(), 16000, 2)
        self.assertEqual(plugin.execute(audio), "go forward ten meters")


if __name__ == "__main__":
    unittest.main()
