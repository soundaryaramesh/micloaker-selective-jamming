import os
import sys
import utils
import librosa
import soundfile as sf
from MPSENet import MPSENet
from config import DATA_FOLDER

target_fs = 16000
# Load the pre-trained model
model = MPSENet.from_pretrained("JacobLinCool/MP-SENet-DNS").to("cuda")
model_fs = model.sampling_rate
assert model_fs == target_fs, 'Incorrect sampling rate!'

def main(mic, freq):
    # create a new directory structure with all the enhanced files
    root_folder = os.path.join(DATA_FOLDER, freq, mic)
    input_dir = '16k-split-data-2-segmented'
    prefix = 'enhanced'
    output_dir = '16k-mpsenet-segmented'
    input_folder = os.path.join(root_folder, input_dir)
    output_folder = os.path.join(root_folder, output_dir)

    os.makedirs(output_folder, exist_ok=True)
    sub_dir_list = [sub_dir for sub_dir in os.listdir(input_folder) if sub_dir.endswith('snr')]
    for sub_dir in sub_dir_list:
        input_sub_folder = os.path.join(input_folder, sub_dir)
        output_sub_folder = os.path.join(output_folder, sub_dir)
        os.makedirs(output_sub_folder, exist_ok=True)
        # run only on 'mo' files !!
        wav_files_list = [wav_file for wav_file in os.listdir(input_sub_folder)
                        if (wav_file.endswith('wav') and wav_file.startswith('16k-mo'))]
        print(wav_files_list)
        for wav_file in wav_files_list:
            sig = utils.read_audio_signal(os.path.join(input_sub_folder, wav_file), target_fs)
            # segment audio before running through model
            # sig = sig[10*target_fs:70*target_fs] 
            enhanced_sig, _, _ = model(sig) #segment_size=10*target_fs
            utils.write_audio_signal(os.path.join(output_sub_folder, f'{prefix}-{wav_file}'), enhanced_sig, target_fs)

if __name__ == '__main__':
    if len(sys.argv) != 3:
        print(f'Format: python3 {sys.argv[0]} <mic> <freq>')
        sys.exit(1)
    mic = sys.argv[1]
    freq = sys.argv[2]
    main(mic, freq)