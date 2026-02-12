This repository contains demo analysis scripts for seminar "Psychophysiology" at the Technical University of Berlin. 
The scripts are created for educational purpose to familiarize students with data curation and analysis process.

****EEG data set****
------------------------
**Overview**    
This dataset contains continuous electroencephalography (EEG) and events data acquired during an auditory oddball task. 
The data were collected to investigate neural and behavioral dynamics during locomotion under controlled experimental conditions.

**Participants**
- Number of participants: 2
- Age range: 24-27
- Sex : M
- Inclusion criteria: no mobility restrictions / right-handed / no skin sensitivity on the scalp  

**Experimental task**
- Name : auditory oddball 
- Task description : participants were instructed to perform an auditory oddball task where they were requested to press a button upon detection of an "odd" stimulus that occured rarely. Odd and standard tones were distinguished in terms of pitch. They performed one block during walking and one during standing. Each block consisted of 200 trials with 20% odd tones. See [paradigm repository](https://github.com/EEGManySteps/eegmanysteps_oddball) for further details about the design. In the baseline task, they were instructed to stand still for three minutes. The initial block was baseline and the order of walking and standing blocks was counterbalanced across participants. Sessions in the data set are labeled as oddballstand, oddballwalk, baseline.    
in the walking session, participants were instructed to walk on a straight line of 12 m in an indoor lab space, holding a smartphone in one hand. The button press was registered by touching the phone screen. At both ends of the straight segment were traffic cones. When reaching a traffic cone, they were instructred to stop, turn around the cone, and position themselves on a straight line again facing the other end before walking again. They were instructed to walk with their regular walking speed that feels natrual to them.
- Number of walking blocks per participant : 1
- Number of standing blocks per participant : 2
- Walking surface : indoor, overground
- Walk distance : 12m 

**EEG hardware**
- System: BrainProducts Liveamp
- Number of channels: 32
- Electrode layout: 10-20
- Reference during recording: FCz
- Ground: FPz
- Sampling frequency: 500
- Online filters: n/a
- Impedance threshold: 10

**Presentation device**
- Device : Android smartphone
- Software : "Presentataion", Neurobehavioural Systems
- Speakr : built-in smartphone speaker

