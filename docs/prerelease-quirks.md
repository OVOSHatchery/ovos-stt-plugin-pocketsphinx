# Pre-release quirks

Behavior changes since the last stable release, newest first. This file is
reset at each stable release.

## 0.2.0a1

- Ported to the pocketsphinx 5 API: `Decoder.default_config()` is gone
  upstream; the decoder is now constructed with keyword arguments. Verified
  transcribing real speech on Python 3.12, 3.13 and 3.14.
- Default English models come from the pocketsphinx package itself
  (`get_model_path()`), not from SpeechRecognition's bundled data.
  SpeechRecognition remains a dependency only for the `AudioData` container.
- Packaging is pyproject-only (setup.py and requirements.txt removed);
  entry point ids are unchanged.
