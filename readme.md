## Description

Mycroft STT plugin for [PocketSphinx](https://cmusphinx.github.io/)

The "plugins" are pip install-able modules that provide new STT engines for mycroft

more info in the [docs](https://mycroft-ai.gitbook.io/docs/mycroft-technologies/mycroft-core/plugins)

NOTE: this is very low accuracy and NOT recommended, it is based on a very old [PR](https://github.com/MycroftAI/mycroft-core/pull/1184) for mycroft-core

## Install

`mycroft-pip install mycroft_stt_plugin_pocketsphinx`

## Configuration

```json
  "stt": {
    "module": "pocketsphinx_stt_plug"
  }
 
```

### Advanced configuration

If you do not want to use the default english model (included) you configure this plugin to use a different one

[Iberian Languages](https://github.com/JarbasIberianLanguageResources/iberian-sphinx) models can be found here, [SourceForge](https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/) also has models for other languages

```json
  "stt": {
    "module": "pocketsphinx_stt_plug",
    "pocketsphinx_stt_plug": {
      "acoustic-model": "path/to/hmm/folder",
      "language-model": "path/to/lm/file.lm",
      "pronounciation-dictionary": "path/to/phonemes/file.dict"
    }
  }
 
```
