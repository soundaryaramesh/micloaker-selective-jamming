import os
import numpy as np

mic_freq_dict = {}
mic_freq_dict['mic3'] = {
    '25000Hz': {
        'speech_rms_list': np.arange(-28, -49, -5),
        'snr_list': [-1, -6, -11, -16, -19.5] #, -21]
    },
    '32800Hz': {
        'speech_rms_list': np.arange(-23, -44, -5),
        'snr_list': [-2, -7, -12, -17, -22] #, -25]
    }
}
mic_freq_dict['mic5'] = {
    '25000Hz': {
        'speech_rms_list': np.arange(-33, -60, -5),
        'snr_list': [3.3, -1.7, -6.7, -11.3, -14.9, -16.9] #, -17.3]
    },
    '32800Hz': {
        'speech_rms_list': [-33, -38, -38, -43, -48], #, -53],
        'snr_list': [3.8, -1.2, -2.9, -7.9, -12.7]#, -17.1]
    }
}

# for segmenting audio
start_time_per_speaker = np.array([10, 10, 10, 10, 10])
# add buffer of 0.5s
duration_per_speaker = 0.5 + np.array([57.72, 60.69, 57.87, 53.40, 59.64])


ROOT_FOLDER = os.path.join(os.path.dirname(os.path.dirname(os.getcwd())), 'micloaker-dataset')
DATA_FOLDER = os.path.join(ROOT_FOLDER, 'test', 'data-collection') #, freq, mic_id, 'split-data-2')
speaker_nums = ['1284', '1320', '1995', '6829', '7176']
configs = ['mo', 'wo', 'wr']
configs_wo_waveguide = ['mo', 'wr']
config_labels = {'mo': 'Mic Only(M)', 'wo': 'Waveguide Only(W)', 'wr': 'Micloaker(W+R)'}
config_labels_wo_waveguide = {'mo': 'Mic Only(M)', 'wr': 'Micloaker(W+R)'}
# sampling rate for ASRs
asr_fs = 16000
asr_models = ['wenet', 'large-v3', 'owsm', 'owsm_v3', 'small', 'medium', 'turbo']

# if mic_id == 'mic3':
#     if freq == '25000Hz':
#         speech_rms_list = np.arange(-28, -54, -5)
#         snr_list = [-1, -6, -11, -16, -19.5, -21] #mic3, 25khz
#     elif freq == '32800Hz':
#         speech_rms_list = np.arange(-23, -49, -5)
#         snr_list = [-2, -7, -12, -17, -22, -25]
# elif mic_id == 'mic5':
#     if freq == '25000Hz':
#         speech_rms_list = np.arange(-33, -65, -5)
#         snr_list = [3.3, -1.7, -6.7, -11.3, -14.9, -16.9, -17.3] #mic5, 25khz
#     elif freq == '32800Hz':
#         speech_rms_list = [-33, -38, -38, -43, -48, -53]
#         snr_list = [3.8, -1.2, -2.9, -7.9, -12.7, -17.1]