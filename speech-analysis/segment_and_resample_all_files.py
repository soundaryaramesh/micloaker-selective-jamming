import os
import math
import utils
from config import speaker_nums, start_time_per_speaker, duration_per_speaker

# create a new directory structure with all the resampled files
root_folder = '/home/soundarya/micloaker/micloaker-dataset/test/data-collection/32800Hz/mic3'
input_dir = 'metaaf'
prefix = '16k'
output_dir = f'{prefix}-{input_dir}-segmented'
input_folder = os.path.join(root_folder, input_dir)
output_folder = os.path.join(root_folder, output_dir)

# other parameters
# 44100 for split-data-2, 48000 for baselines
input_fs = 48000 #44100
output_fs = 16000

def get_segmentation_frames(fname, fs, snr_dir):
    for idx, speaker_num in enumerate(speaker_nums):
        if speaker_num in fname:
            # everything except 1284, for the 25k folder
            if (speaker_num in speaker_nums[1:]) and (snr_dir == '-43db-speech--16db-snr'):
                print('reached condition!!!')
                start_time = 7
            else:
                start_time = start_time_per_speaker[idx]
            end_time = start_time + duration_per_speaker[idx]
            start_frame = math.ceil(start_time*fs)
            end_frame = math.ceil(end_time*fs)
            print(f'{fname}: {start_time}:{end_time}, {start_frame}:{end_frame}')
            return start_frame, end_frame

os.makedirs(output_folder, exist_ok=True)
sub_dir_list = [sub_dir for sub_dir in os.listdir(input_folder) if sub_dir.endswith('snr')]
for sub_dir in sub_dir_list:
    input_sub_folder = os.path.join(input_folder, sub_dir)
    output_sub_folder = os.path.join(output_folder, sub_dir)
    os.makedirs(output_sub_folder, exist_ok=True)
    # modified !!
    wav_files_list = [wav_file for wav_file in os.listdir(input_sub_folder)
                    if wav_file.endswith('wav')] # and wav_file.startswith('mo')]
    for wav_file in wav_files_list:
        sig = utils.read_audio_signal(os.path.join(input_sub_folder, wav_file), input_fs)
        # segmenting the input !!
        start_frame, end_frame = get_segmentation_frames(wav_file,input_fs, sub_dir)
        sig = sig[start_frame:end_frame]
        resampled_sig = utils.compute_resampled_data(sig, input_fs, output_fs)
        utils.write_audio_signal(os.path.join(output_sub_folder, f'{prefix}-{wav_file}'), resampled_sig, output_fs)


