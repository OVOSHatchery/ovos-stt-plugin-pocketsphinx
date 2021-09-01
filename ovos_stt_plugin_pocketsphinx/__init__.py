from ovos_stt_plugin_pocketsphinx.recognizer import PocketSphinxRecognizer
from os.path import isdir, isfile
from ovos_plugin_manager.templates.stt import STT
from ovos_utils.log import LOG


class PocketSphinxSTTPlugin(STT):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        pho = self.config.get("pronounciation-dictionary")
        lm = self.config.get("language-model")
        hmm = self.config.get("acoustic-model")

        if self.lang.startswith("en"):
            dhmm, dlm, dph = PocketSphinxRecognizer.get_default_english_model()
            if not pho or not isfile(pho):
                LOG.info("Falling back to default english dictionary")
                pho = dph
            if not lm or not isfile(lm):
                LOG.info("Falling back to default english language model")
                lm = dlm
            if not hmm or not isdir(hmm):
                LOG.info("Falling back to default english acoustic model")
                hmm = dhmm

        self.recognizer = PocketSphinxRecognizer(hmm, lm, pho)

    def execute(self, audio, language=None):
        return self.recognizer.recognize(audio)

