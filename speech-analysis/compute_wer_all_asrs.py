import numpy as np
import os
import sys
import pandas as pd
from config import (
    mic_freq_dict, ROOT_FOLDER, DATA_FOLDER, speaker_nums #, configs, config_labels#, asr_models
)
from utils import retrieve_ref_text, compute_wer_for_speaker
# TO MODIFY !!
asr_models = ['wenet']
configs = ['mo']
# TO MODIFY !!
config_labels = {'mo': 'MPSeNet-segmented'}

def main(mic, freq):
    # file structure
    # TO MODIFY !!
    wav_folder = os.path.join(DATA_FOLDER, freq, mic, '16k-mpsenet-segmented')
    wer_folder = os.path.join(wav_folder, 'wer-results')
    os.makedirs(wer_folder, exist_ok=True)
    # read from config
    speech_rms_list = mic_freq_dict[mic][freq]['speech_rms_list']
    snr_list = mic_freq_dict[mic][freq]['snr_list']
    n_rms = np.size(speech_rms_list)
    assert np.size(snr_list) == n_rms
    # header for CSV files
    header_row1 = [[model]*len(configs) for model in asr_models]
    header_row1 = list(np.concatenate(header_row1))
    header_row2 = list(config_labels.values())*len(asr_models)
    header = [header_row1, header_row2]
    print(header)
    assert len(header_row1) == len(header_row2)
    # get reference texts
    gt_text_dict = retrieve_ref_text(ROOT_FOLDER, speaker_nums)
    # iterate through all SNR folders
    n_rms = np.size(speech_rms_list)
    assert np.size(snr_list) == n_rms
    for idx in range(n_rms):
        snr_name = '{}db-speech-{}db-snr'.format(speech_rms_list[idx], snr_list[idx])
        print('Folder Name:', snr_name)
        snr_dir = os.path.join(wav_folder, snr_name) 
        save_path = os.path.join(wer_folder, snr_name+'-wer_all_models.csv')
        wer_dict = {}
        for speaker_num in speaker_nums:
            ref = gt_text_dict[speaker_num]
            print('='*50)
            print('Speaker Num: {}'.format(speaker_num))
            speaker_dict = compute_wer_for_speaker(snr_dir, speaker_num, ref, mic, freq, asr_models, configs, config_labels)
            wer_dict[speaker_num] = speaker_dict.values()
        df = pd.DataFrame.from_dict(wer_dict, orient='index', columns=header)
        # breakpoint()
        df.to_csv(save_path)
        # break

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Correct format: python3 {sys.argv[0]} <mic> <freq>')
        sys.exit(1)
    mic = sys.argv[1]
    freq = sys.argv[2]
    main(mic, freq)
    
