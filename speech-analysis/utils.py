import os
import re
import glob
import librosa
import contractions
import numpy as np
from jiwer import wer
import soundfile as sf

# read single channel audio files
def read_audio_signal(file_path, fs, mono=True):
	sig, sig_fs = librosa.load(file_path, sr=fs, mono=mono)
	assert sig_fs == fs
	return sig

# resample audio signal
def compute_resampled_data(sig, orig_fs, target_fs):
	resampled_sig = librosa.resample(sig, orig_sr=orig_fs, target_sr=target_fs)
	return resampled_sig

# write audio signals
def write_audio_signal(file_path, sig, fs):
	sf.write(file=file_path, data=sig, samplerate=fs)

def compute_hypothesis(snr_dir, config, mic_id, speaker_num, freq, chosen_model):
	"""Finds the hypothesis file using a glob pattern, reads it, normalizes the text, and returns it."""
	fname_pattern = os.path.join(snr_dir, f'*{config}_{mic_id}*{speaker_num}*{freq}_*_{chosen_model}.txt')
	matching_files = glob.glob(fname_pattern)
	if len(matching_files) == 0:
		assert ('infomix' in snr_dir) or ('metaaf' in snr_dir)
		fname_pattern = os.path.join(snr_dir, f'*{speaker_num}*_{chosen_model}.txt')
		matching_files = glob.glob(fname_pattern)
	assert len(matching_files) == 1, f'Expected exactly one matching file for pattern: {fname_pattern}'
	with open(matching_files[0], 'r') as tts_file:
		hypothesis = tts_file.read()
	hypothesis = normalize_text(hypothesis)
	assert 'CUDA' not in hypothesis, f'incorrect! {hypothesis}'
	return hypothesis

def compute_wer_for_speaker(snr_dir, speaker_num, ref, mic, freq, asr_models, configs, config_labels):
	"""Computes the WER for each model/config combination for a given speaker.
	Returns a dictionary mapping 'model-config' strings to their computed WER values.
	"""
	speaker_dict = {}
	for chosen_model in asr_models:
		for config in configs:
			hypothesis = compute_hypothesis(snr_dir, config, mic, speaker_num, freq, chosen_model)
			computed_wer = wer(ref, hypothesis) * 100
			print(f'{chosen_model},{config_labels[config]}:\tWER={computed_wer}')
			speaker_dict[f'{chosen_model}-{config}'] = computed_wer
	return speaker_dict

def normalize_text(text):
	"""
	Normalize text by:
	- Expanding contractions (e.g., "I'm" -> "I AM")
	- Converting to uppercase
	- Preserving hyphens between words (e.g., "well-known" -> "WELL KNOWN")
	- Removing other punctuation
	- Removing extra spaces
	"""
	# Replace underscore-like markers with spaces
	text = text.replace('▁', ' ')
	# Expand contractions (e.g., "I'm" → "I AM")
	text = contractions.fix(text)
	# Convert to uppercase
	text = text.upper()
	# Preserve hyphens between words but remove other punctuation
	text = re.sub(r"(\w+)-(\w+)", r"\1 \2", text)  # Converts "well-known" → "WELL KNOWN"
	text = re.sub(r"[^\w\s]", "", text)  # Remove remaining punctuation
	# Remove extra spaces
	text = re.sub(r"\s+", " ", text).strip()
	return text

def retrieve_ref_text(ref_folder, speaker_nums):
	gt_text_dict = {}
	for speaker_num in speaker_nums:
		# print('-'*100)
		gt_transcription_path = os.path.join(ref_folder, 'target_'+speaker_num+'.txt')
		with open(gt_transcription_path, 'r') as gt_file:
			gt_text = gt_file.read()
			gt_text = normalize_text(gt_text)
			gt_text_dict[speaker_num] = gt_text
	# print('Ground Truth Transcription: ')
	# print(gt_text_dict)
	return gt_text_dict

# useful for MPSeNet
def split_wav_by_time(file_path, sr, output_folder, segment_dur=10):
	"""Splits wav file into segment_dur-sec segments."""
	os.makedirs(output_folder, exist_ok=True)
	data, sr = librosa.load(file_path, sr=sr, mono=True)
	split_files = []
	duration = librosa.get_duration(y=data, sr=sr)
	num_splits = int(np.ceil(duration / segment_dur))
	for split_idx in range(num_splits):
		output_file = os.path.join(output_folder, f"{os.path.basename(file_path).replace('.wav', '')}_split{split_idx+1}.wav")
		if os.path.exists(output_file):
			split_files.append(output_file)
			continue
		start_sample = split_idx * segment_dur * sr
		end_sample = min((split_idx + 1) * segment_dur * sr, len(data))
		split_audio = data[start_sample:end_sample]
		sf.write(output_file, split_audio, sr)
		split_files.append(output_file)
	return split_files

