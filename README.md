# MiCloaker: Selective Microphone Recording with Acoustic Structures
This repo contains 3D-printing files and code to replicate MiCloaker's hardware setup and results. 

## Hardware Setup
We place the speakers and the microphones on two different [projector stands](https://shopee.sg/Projector-Tripod-Projector-Floor-Stand-Foldable-Laptop-Stand-Speaker-Stand-Adjustable-90cm-180cm-Tray-Projector-Stand-Heavy-Duty-i.873500605.10398658831), at a distance of 70 cm, such that the microphone and the ultrasound speaker are in-line with each other (i.e., azimuth and elevation is 0 degrees). We use the following components to 
- Ultrasound Transducers: [25kHz](https://www.cuidevices.com/product/resource/cusa-t80-12-2600-th.pdf), [32kHz](https://www.mouser.com/datasheet/2/911/T328S16-1371205.pdf). We use the transducers to make two 3x3 arrays for transmitting the carrier frequency and the modulated signals.
- Amplifier for Ultrasound Transducers: [FPA101A](https://www.aliexpress.com/item/33023103749.html?spm=a2g0o.order_list.order_list_main.5.565d18028oncPS) 
- Audible Speaker (for transmitting speech): Adam Audio A3X studio monitor with flat frequency response in the audible range. 
- MiCloaker structures: 3D-print the prototypes mentioned in the _prototype-files_ folder. We used Asiga Max X27 printer and MakerBot Sketch 3D-printer to 3D-print the resonators and waveguide, respectively.
- Microphone: DF-Robot S15OT421 Breakout Board.
- Audio Interfaces for Connecting Speakers, Microphones to Laptop: [Scarlett Solo](https://focusrite.com/products/scarlett-solo), [Behringer 202HD](https://www.behringer.com/product.html?modelCode=0805-AAR).
- Other Useful Tools: [Arm Clamp](https://shopee.sg/Solder-Helping-Hands-Soldering-Aids-Hand-Tool-with-Flexible-Arms-Clamp-Swivel-i.328435272.23656935887) to support the microphone board in place, [Bostik Blu Tack](https://shopee.sg/Bostik-Blu-tack-75g-Blue-White-i.304740536.10034505185) to prevent audio leakage around the microphone. 

## Ultrasound Jamming Signal Creation
We utilize the technique proposed in the [InfoMasker paper](https://www.ndss-symposium.org/ndss-paper/infomasker-preventing-eavesdropping-using-phoneme-based-noise/) to create lower sideband phoneme-based ultrasound jamming noise. We present sample files for ultrasound jamming in the _sample-files_ folder.  

## Ensuring Safety Limits for Ultrasound Signals
We record the ultrasound signals alone using a microphone (without any amplification) to ensure that the recorded level is within the safety limits. We follow the guidelines mentioned [here](https://www.sciencedirect.com/science/article/pii/S0079610706000885). In addition, while performing experiments, we use [3M Peltor X5 earmuffs](https://www.3m.com.sg/3M/en_SG/p/d/v000137089/) for safety. 

## SJR Calibration
To record jammed speech at different SJRs as mentioned in the paper, we perform calibration where-in we capture the jamming noise and the audible speech separately. We continuously tune the transmission volume of the audible speech signal till we achieve the required SJR. 

## Demo Results
We share a few representative output audio files for both carrier frequencies, at a wide range of SNRs in the _demo-files_ folder. 
