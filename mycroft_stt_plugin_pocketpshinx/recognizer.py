import speech_recognition as sr
import os
from os.path import join, isdir, dirname, isfile
from pocketsphinx import Jsgf, FsgModel, Decoder


class PocketSphinxRecognizer:
    def __init__(self,
                 acoustic_parameters_directory=None,
                 language_model_file=None,
                 phoneme_dictionary_file=None):

        if not isdir(acoustic_parameters_directory):
            raise sr.RequestError(
                "missing PocketSphinx language model parameters directory: "
                "\"{}\"".format(acoustic_parameters_directory))

        if not isfile(language_model_file):
            raise sr.RequestError(
                "missing PocketSphinx language model file: \"{}\"".format(
                    language_model_file))

        if not isfile(phoneme_dictionary_file):
            raise sr.RequestError(
                "missing PocketSphinx phoneme dictionary file: \"{}\"".format(
                    phoneme_dictionary_file))

        # create decoder object
        config = Decoder.default_config()
        config.set_string("-hmm", acoustic_parameters_directory)
        config.set_string("-lm", language_model_file)
        config.set_string("-dict", phoneme_dictionary_file)
        config.set_string("-logfn", os.devnull)
        self.decoder = Decoder(config)

    @staticmethod
    def get_default_english_model():
        language_directory = join(dirname(sr.__file__),
                                  "pocketsphinx-data", "en-US")
        hmm = join(language_directory, "acoustic-model")
        lm = join(language_directory, "language-model.lm.bin")
        pho = join(language_directory, "pronounciation-dictionary.dict")
        return hmm, lm, pho

    def recognize(self, audio_data, keyword_entries=None, grammar=None):
        assert isinstance(audio_data,
                          sr.AudioData), "``audio_data`` must be audio data"
        assert keyword_entries is None or all(
            isinstance(keyword,
                       (type(""), type(u""))) and 0 <= sensitivity <= 1
            for keyword, sensitivity in
            keyword_entries), "``keyword_entries`` must be ``None`` or" \
                              " a list of pairs of strings and " \
                              "numbers between 0 and 1"
        # obtain audio data
        raw_data = audio_data.get_raw_data(convert_rate=16000,
                                           convert_width=2)
        # obtain recognition results
        if keyword_entries is not None:  # explicitly specified set of keywords
            with sr.PortableNamedTemporaryFile("w") as f:
                # generate a keywords file
                f.writelines(
                    "{} /1e{}/\n".format(keyword, 100 * sensitivity - 110)
                    for keyword, sensitivity in keyword_entries)
                f.flush()
                # perform the speech recognition with the keywords file
                self.decoder.set_kws("keywords", f.name)
                self.decoder.set_search("keywords")
                self.decoder.start_utt()  # begin utterance processing
                self.decoder.process_raw(raw_data, False,
                                         True)
                self.decoder.end_utt()  # stop utterance processing
        elif grammar is not None:  # a path to a FSG or JSGF grammar
            if not os.path.exists(grammar):
                raise ValueError(
                    "Grammar '{0}' does not exist.".format(grammar))
            grammar_path = os.path.abspath(os.path.dirname(grammar))
            grammar_name = os.path.splitext(os.path.basename(grammar))[0]
            fsg_path = "{0}/{1}.fsg".format(grammar_path, grammar_name)
            if not os.path.exists(
                    fsg_path):  # create FSG grammar if not available
                jsgf = Jsgf(grammar)
                rule = jsgf.get_rule("{0}.{0}".format(grammar_name))
                fsg = jsgf.build_fsg(rule, self.decoder.get_logmath(), 7.5)
                fsg.writefile(fsg_path)
            else:
                fsg = FsgModel(fsg_path, self.decoder.get_logmath(), 7.5)
            self.decoder.set_fsg(grammar_name, fsg)
            self.decoder.set_search(grammar_name)
            self.decoder.start_utt()
            self.decoder.process_raw(raw_data, False,
                                     True)
            self.decoder.end_utt()  # stop utterance processing
        else:  # no keywords, perform freeform recognition
            self.decoder.start_utt()  # begin utterance processing
            self.decoder.process_raw(raw_data, False,
                                     True)
            self.decoder.end_utt()  # stop utterance processing
        # return results
        hypothesis = self.decoder.hyp()
        if hypothesis is not None:
            return hypothesis.hypstr
        raise sr.UnknownValueError()  # no transcriptions available

    def recognize_wav(self, file_path, keyword_entries=None, grammar=None):
        r = sr.Recognizer()
        with sr.AudioFile(file_path) as source:
            audio = r.record(source)
        return self.recognize(audio, keyword_entries, grammar)

