import os
from utils import read_audio_signal, normalize_text
import numpy as np
import random
import torch
import librosa
import warnings
warnings.filterwarnings("ignore", message=".*The 'nopython' keyword.*")
import wenet
import whisper
if os.environ.get("CONDA_DEFAULT_ENV") == "micloaker-espnet":
    from espnet2.bin.s2t_inference import Speech2Text
    from espnet2.bin.s2t_inference_ctc import Speech2TextGreedySearch
import sys
seed = 100
torch.manual_seed(seed)
np.random.seed(seed)
random.seed(seed)

class ASRComputation:
    def __init__(self, asr_type='', fs=16000):
        self.asr_type = asr_type
        self.fs = fs
        self.snr_folder = ''
        self.transcribed_text = ''
        self.audio_fname = ''
        self.text_fname = ''
        self.asr_model = self.load_model()
    
    def load_model(self):
        if self.asr_type == 'wenet':
            asr_model = wenet.load_model('english')
        elif self.asr_type in ['small', 'medium', 'large', 'turbo', 'large-v3', 'large-v2']: # whisper models
            asr_model = whisper.load_model(self.asr_type)
        elif self.asr_type == 'owsm':
            assert os.environ.get("CONDA_DEFAULT_ENV") == "micloaker-espnet", 'Incorrect conda env!'
            asr_model = Speech2Text.from_pretrained(
                model_tag="espnet/owsm_v3.1_ebf",
                device="cuda",
                beam_size=1,
                ctc_weight=0.0,
                maxlenratio=0.0,
                batch_size=1,
                # below are default values which can be overwritten in __call__
                lang_sym="<eng>",
                task_sym="<asr>",
            )
        elif self.asr_type == 'owsm_v3':
            assert os.environ.get("CONDA_DEFAULT_ENV") == "micloaker-espnet", 'Incorrect conda env!'
            asr_model = Speech2Text.from_pretrained(
                model_tag="espnet/owsm_v3",
                device="cuda",
                beam_size=1,
                ctc_weight=0.0,
                maxlenratio=0.0,
                batch_size=1,
                # below are default values which can be overwritten in __call__
                lang_sym="<eng>",
                task_sym="<asr>",
            )
        # elif self.asr_type == 'owsm_ctc':
        #     assert os.environ.get("CONDA_DEFAULT_ENV") == "micloaker-espnet", 'Incorrect conda env!'
        #     asr_model = Speech2TextGreedySearch.from_pretrained(
        #         model_tag="espnet/owsm_ctc_v3.1_1B",
        #         device="cuda",
        #         generate_interctc_outputs=False,
        #         # beam_size=1,
        #         # ctc_weight=0.0,
        #         # maxlenratio=0.0,
        #         # batch_size=1,
        #         # below are default values which can be overwritten in __call__
        #         lang_sym="<eng>",
        #         task_sym="<asr>",
        #     )
        else:
            print('Incorrect ASR Type')
            asr_model = np.nan
        return asr_model
    
    def set_folder_name(self, snr_folder):
        self.snr_folder = snr_folder

    def set_text_fname(self, text_fname):
        self.text_fname = text_fname

    def set_transcribed_text(self, text):
        self.transcribed_text = text

    def compute_transcription(self, audio_fpath):
        if self.asr_type == 'wenet':
            transcribed_text = self.asr_model.transcribe(audio_file=audio_fpath)['text']
        elif self.asr_type in ['small', 'medium', 'large', 'turbo', 'large-v3', 'large-v2']: # whisper models
            try:
                transcribed_text = self.asr_model.transcribe(audio_fpath,
                                                    # temperature=0.7,
                                                    # condition_on_previous_text=False,    
                                                    # best_of=5,
                                                    # hallucination_silence_threshold=2,
                                                    # no_speech_threshold=0.6,
                                                    language='en')['text']
            except:
                transcribed_text = 'cuda error'
                print(f'ERROR!! {audio_fpath}')
        elif 'owsm' in self.asr_type:
            sig = read_audio_signal(audio_fpath, self.fs)
            try:
                result = self.asr_model.decode_long(sig)
                transcription_list = [res[2] for res in result]
                transcribed_text = ' '.join(transcription_list)
            except:
                transcribed_text = 'cuda error'
                print(f'ERROR!! {audio_fpath}')
        # print(transcribed_text)
        transcribed_text = normalize_text(transcribed_text)
        return transcribed_text

    def convert_to_text(self, audio_fname):
        self.audio_fname = audio_fname
        self.set_text_fname('')
        audio_fpath = os.path.join(self.snr_folder, self.audio_fname)
        _, sig_fs = librosa.load(audio_fpath, sr=self.fs)
        assert sig_fs == self.fs, 'Sampling rates do not match!'
        self.set_transcribed_text(self.compute_transcription(audio_fpath))
        return self.transcribed_text
    
    def save_transcribed_text(self):
        assert self.text_fname == '', 'Incorrect text file name!'
        self.set_text_fname(self.audio_fname.replace('.wav', f'_{self.asr_type}.txt'))
        text_fpath = os.path.join(self.snr_folder, self.text_fname)
        with open(text_fpath, 'w') as text_file:
            text_file.write(self.transcribed_text)
        print(f'Text saved successfully to: {self.text_fname}')