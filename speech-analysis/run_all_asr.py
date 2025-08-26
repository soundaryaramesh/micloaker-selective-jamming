import subprocess

asr_type_list = ['owsm_v3'] #['small', 'medium', 'turbo'] #['owsm'] #['wenet', 'large-v3', 'owsm']
freq_list = ['25000Hz', '32800Hz']
mic = 'mic3'

script_name = 'perform_asr.py'
for freq in freq_list:
    for asr_type in asr_type_list:
        subprocess.run(['python3', script_name, mic, freq, asr_type])