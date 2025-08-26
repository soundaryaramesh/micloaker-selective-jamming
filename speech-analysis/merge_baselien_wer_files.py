import os
import sys
import glob
import numpy as np
import pandas as pd
from config import (
    mic_freq_dict, DATA_FOLDER, speaker_nums
)

def main(mic, freq, asr_type='wenet'):
    freq_mic_folder = os.path.join(DATA_FOLDER, freq, mic)
    wer_dir = 'wer-results'
    # TO MODIFY !!
    main_folder = os.path.join(freq_mic_folder, '16k-split-data-2', wer_dir)
    mpsenet_folder = os.path.join(freq_mic_folder, '16k-mpsenet-segmented', wer_dir)
    infomix_folder = os.path.join(freq_mic_folder, '16k-infomix-segmented', wer_dir)
    metaaf_folder = os.path.join(freq_mic_folder, '16k-metaaf-segmented', wer_dir)
    folder_list = [main_folder]*2
    folder_list.extend([mpsenet_folder, infomix_folder, metaaf_folder])
    print(folder_list)
    header_row1 = [asr_type]*5
    # TO MODIFY !!
    header_row2 = ['Mic Only(M)', 'Micloaker(W+R)', 'MPSeNet-segmented', 'InfoMix-segmented', 'MetaAF-segmented']
    assert len(header_row1) == len(header_row2)
    # read all the csv files and merge them together
    speech_rms_list = mic_freq_dict[mic][freq]['speech_rms_list']
    snr_list = mic_freq_dict[mic][freq]['snr_list']
    n_rms = np.size(speech_rms_list)
    assert np.size(snr_list) == n_rms
    for idx in range(n_rms):
        snr_name = '{}db-speech-{}db-snr'.format(speech_rms_list[idx], snr_list[idx])
        print('Folder Name:', snr_name)
        df_list = []
        for idx, (folder_path, row1_label, row2_label) in enumerate(zip(folder_list, header_row1, header_row2)):
            csv_fname_pattern = os.path.join(folder_path, f'*{snr_name}*_models.csv')
            matching_files = glob.glob(csv_fname_pattern)
            assert len(matching_files) == 1, f'Expected exactly one matching file for pattern: {csv_fname_pattern}'
            df_idx = pd.read_csv(matching_files[0], header=[0,1])
            # check that the speaker order is the same
            assert [str(spk_num) for spk_num in df_idx.iloc[:, 0].to_list()] == speaker_nums
            chosen_df_idx = df_idx[[(row1_label, row2_label)]]
            df_list.append(chosen_df_idx)
        merged_df = pd.concat(df_list, axis=1)
        save_path = os.path.join(main_folder, f'{snr_name}_{asr_type}_with_baselines.csv')
        merged_df.to_csv(save_path, index=False)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Correct format: python3 {sys.argv[0]} <mic> <freq>')
        sys.exit(1)
    mic = sys.argv[1]
    freq = sys.argv[2]
    main(mic, freq)