## Description

Mycroft STT plugin for [PocketSphinx](https://cmusphinx.github.io/)

NOTE: this is very low accuracy and NOT recommended, it is based on a very old [PR](https://github.com/MycroftAI/mycroft-core/pull/1184) for mycroft-core

## Install

`pip install ovos-stt-plugin-pocketsphinx`

## Configuration

```json
  "stt": {
    "module": "ovos-stt-plugin-pocketsphinx"
  }
 
```

### Advanced configuration

If you do not want to use the default english model (included) you configure this plugin to use a different one

[Iberian Languages](https://github.com/JarbasIberianLanguageResources/iberian-sphinx) models can be found here, [SourceForge](https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/) also has models for other languages

```json
  "stt": {
    "module": "ovos-stt-plugin-pocketsphinx",
    "ovos-stt-plugin-pocketsphinx": {
      "acoustic-model": "path/to/hmm/folder",
      "language-model": "path/to/lm/file.lm",
      "pronounciation-dictionary": "path/to/phonemes/file.dict"
    }
  }
 
```
