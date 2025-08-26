# import libraries
import os
import numpy as np
import sys
from config import (
    mic_freq_dict, DATA_FOLDER, asr_fs
)
from asr_computation import ASRComputation

if __name__ == '__main__':
    if len(sys.argv) != 4:
        print(f'Correct format: python3 {sys.argv[0]} <mic> <freq> <asr-type>')
        sys.exit(1)
    mic = sys.argv[1]
    freq = sys.argv[2]
    asr_type = sys.argv[3]
    # read from config
    # to be modified !!
    wav_folder = os.path.join(DATA_FOLDER, freq, mic, '16k-mpsenet-segmented')
    speech_rms_list = mic_freq_dict[mic][freq]['speech_rms_list']
    snr_list = mic_freq_dict[mic][freq]['snr_list']
    n_rms = np.size(speech_rms_list)
    assert np.size(snr_list) == n_rms
    # read all files of interest
    asr_obj = ASRComputation(asr_type, asr_fs) 
    for idx in np.arange(n_rms):
        print('-'*100)
        snr_dir = '{}db-speech-{}db-snr'.format(speech_rms_list[idx], snr_list[idx])
        print('SNR Directory:', snr_dir)
        snr_folder = os.path.join(wav_folder, snr_dir)
        asr_obj.set_folder_name(snr_folder)
        wav_files = [f for f in os.listdir(snr_folder) if f.endswith('.wav')]
        for wav_file in wav_files:
            print(f'Audio File: {wav_file}')
            transcribed_text = asr_obj.convert_to_text(wav_file)
            print(transcribed_text)
            asr_obj.save_transcribed_text()
            # breakpoint()
            # break
        # break