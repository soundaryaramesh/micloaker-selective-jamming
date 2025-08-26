import os
import utils

# create a new directory structure with all the resampled files
root_folder = '/home/soundarya/micloaker/micloaker-dataset/test/data-collection/32800Hz/mic3'
input_dir = 'split-data-2'
prefix = '16k'
output_dir = f'{prefix}-{input_dir}'
input_folder = os.path.join(root_folder, input_dir)
output_folder = os.path.join(root_folder, output_dir)

# other parameters
input_fs = 44100
output_fs = 16000

if not os.path.exists(output_folder):
    os.makedirs(output_folder)

sub_dir_list = [sub_dir for sub_dir in os.listdir(input_folder) if sub_dir.endswith('snr')]
for sub_dir in sub_dir_list:
    input_sub_folder = os.path.join(input_folder, sub_dir)
    output_sub_folder = os.path.join(output_folder, sub_dir)
    if not os.path.exists(output_sub_folder):
        os.makedirs(output_sub_folder)
    wav_files_list = [wav_file for wav_file in os.listdir(input_sub_folder) if wav_file.endswith('wav')]
    for wav_file in wav_files_list:
        sig = utils.read_audio_signal(os.path.join(input_sub_folder, wav_file), input_fs)
        resampled_sig = utils.compute_resampled_data(sig, input_fs, output_fs)
        utils.write_audio_signal(os.path.join(output_sub_folder, f'{prefix}-{wav_file}'), resampled_sig, output_fs)




