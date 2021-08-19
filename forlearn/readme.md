# faceprf

Use face stimuli to map population receptive field and study the neural mechanisms of attention 

REFERENCE: Kay, K. N., Weiner, K. S., & Grill-Spector, K. (2015). Attention reduces spatial uncertainty in human ventral temporal cortex. *Current Biology*, *25*(5), 595-600.



## Developer

Ru-Yuan Zhang ruyuanzhang@gmail.com



## History

2021/07/02 RYZ create it



## Task details

### Files:

- `runfaceprf.py` is the script that runs the experiment
- `mriexpfun.py` is a collection of utility functions (e.g., eyetracking code) that may be used in the main code.
- `faceprfdesign.npz` is a file that contains stimulus presentation order and image



### How to run the experiment at 7TPS:

- Close all background processes

On running the experiment:
- Note that the images are loaded the first time the script is run.
  On subsequent calls, the previously loaded images are re-used (to save time).
  Also, the subject ID is preserved and not requested again.
- If you want to start from scratch, just do a clear all and run the script again.
- Important: to tweak the experiment, edit the parameters at the top of the script.
- Note that the experiment script automatically runs kendrickstartup.m which
  sets up critical MATLAB path stuff (including PsychToolbox).

Experiment information:
- Each experimental run is 330 seconds long (5.5 min). There are 12 runs in total.
- There is a short load delay at the beginning of the experiment. Make sure that
  the stimulus computer reports that it is ready for the trigger. Once this is
  reached, the computer waits for the trigger key, at which point the experiment starts.
- The experiment consists of 15-s rest, followed by 60 trials (5-s each), and then
  15-s rest again. Note that some of the 60 trials are blank trials (detailed below).
- The stimuli consist of a 5 x 5 grid of face positions. The faces are "medium-sized"
  faces that have 3.2-deg diameter (the "circle" that describes the spatial extent
  of the faces has 3.2-deg diameter). The numbering of the grid is left to right, then
  top to bottom (e.g., the upper-left is 1, the upper right is 5, etc.).
- Regarding the grid, the displacement is 164 pixels which corresponds to 1.8 deg.
  Thus, in both the horizontal and vertical dimensions, the centers of the faces
  vary from -3.6, -1.8, 0, 1.8, and 3.6 deg relative to the center of the display.
- The "contrast images" that I've prepared are available at:
    /home/stone-ext1/kendrick/stimulusfiles/workspace_categoryC8h.mat
  in the variable 'conimages'.
- We pull faces from a bank of 7 viewpoints x 95 identities = 665 faces.
  Faces are assigned positive integers (e.g., 1-7 correspond to the first person).
  Viewpoints are random and are constrained such that the same viewpoint does
  not repeat twice in a row for the 4 faces that compose a trial.
  However, we place very specific constraints on the identities (detailed below).
- During the course of the run, there is a stream of digits. These digits
  alternate between white/black and are 0.3 deg x 0.3 deg in size.
  The digits are pseudorandom (detailed below).
- The experiment operates at 12 frames per second. Thus, at 120 Hz, each frame
  lasts for 10 monitor refreshes.
- In each run, each of 25 stimuli are presented two times each.
  In addition to these 50 stimulus trials, there are 10 blank trials (randomly thrown in).
- The total run structure is 15 + (25*2 + 10)*5 + 15 = 330 seconds.
- Over the course of one scan session (12 runs), each of the [25 stimuli x
  2 tasks] = 50 conditions are presented 12 times each.
- To quit a run early, press `q`.
- After a run completes, a .mat file is written out with timing information
  and keypress information. These are important; keep these .mat files!

On anticipatory/predictive confounding effects:
- The digit task is pretty steady-state, so it probably won't be susceptible to
  these sorts of effects.
- As for the face task, the trial structure is very regular and very predictable --
  the subject is engaged pretty constantly over time. There are, I suppose, occasional
  blank trials and so in these cases, the subject may anticipate having to "start
  up" again (while she is waiting for the blank trial to finish). But these make
  up a small fraction of the dataset, so probably not a big problem...

On special stimulus ordering:
- The experimenter should pre-generate stimulus files and indicate the exact
  order with which to use the pre-generated stimulus files during the experiment.
- This is tricky business and the experimenter should keep track of all these files.
- Our strategy is to pre-generate a fixed set of 6 physical instantiations. These
  instantiations keep a hard record of ordering of stimulus frames and the ordering
  of digits. We re-use these instantiations for the two tasks:
    physical: 123456 654321
        task: ABABAB ABABAB
  For subsequent scan sessions, the plan is to shuffle these 12 instantiations
  (preserving the physical-task correspondency). This way, we will be able to
  perform averaging of runs across sessions (the "smashing" idea).

On tasks:
- There is a digit task (A) and a face task (B).
- See runfaceprf_subjectinstructions.txt for what subjects should know.

On trial design:
- The trials are 5-s. There are 4 faces per trial using 1000/0 structure.
  Thus, there are 4 1-s faces followed by 1-s of gap.
  We can summarize this as "4/1".
- We define an event as the repetition of face identity.
- There is 10% likelihood that there is no event for a given trial.
- For the other 90% of the trials, we generate an event on face frames 2-4
  with 0.25 likelihood on each frame. If no event is generated using this
  method, we manually force an event by inserting one event randomly at
  one of the frames 2-4.

On digit design:
- We match the rate of digits to the rate of the face task.
- Specifically, we have determined that the face task will, on average, involve
  53 button presses in 300 s (including the influence of rest trials).
- This means one button press approximately every 5.66 s.
- Since a new digit is encountered every 1/2 s, and since 5.66/(1/2) = 11.32,
  the probability of digit repetition is set to 1/11.32 (in the experiment script).
  Note that this allows for the possibility of 3 or more digits in a row.

Some subjective notes on the experiment:
- Black and white digits are not very visible when the faces are in the center.
- Face identity task is really hard in the periphery. That's good, I think.

Stimulus-size issues:
- The stimuli are hard-coded for presentation on the.We assume a display resolution of 1024 x 768, and we assume that the 1080 vertical pixels correspond to .
- The stimuli are sized such that they fully fit within a 11-deg square region of the display.

Eyetracker:
- Yes, you want to eyetrack, since there is covert spatial attention involved.
- The stimulus code is designed to automatically interface with the Eyelink eyetracker. We have `setupeyetrackmri` and `closeupeyetrackmri` functions to initiate and stop eyetracking
- Eyetracking data are downloaded to the stimulus computer immediately after each run is completed.

Display-calibration issues:
- Note that when presenting on regular displays, the stimuli will look "too dark".
- The uint8 value for the gray background is 101.

Timing issues:
- The experiment code locks to the refresh rate of the display.
- on 2021-07-02, RYZ checked the timing of the code. By setting `timefactor=0.17`, we can get a delay within 100ms. But this strongly depends on the concurrent memory consumption. So please close all other background processes!!!
- For fMRI data, we should just resample the time-series to be in line with the 1.000316 number.

Subjective experience:
- KK: trials are sometimes very easy, sometimes hard. subjects need to be on their toes.
- KK: very challenging to sustain focus for all 12 runs! need motivated subjects!

Screen capture:
- Note that he used a special "non-squaring" version of the stimulus, so that when
  we view the movie file on our regular displays, the luminance values are like what
  they actually are during the experiment.

### Contents of the behavioral .mat file:

- Here is a description of all the relevant variables that one might need to know
  in order to analyze the behavioral data:
  'timeframes' - 1 x frames. The numbers indicate the actual empirical time
                 corresponding to the presentation of each stimulus frame.
                 Time is relative to the time of the first frame.
  'timekeys' - N x 2 cell. This tells you what keys/buttons/triggers were pressed and when.
  'trialpattern' - trials x stimuli. 1s indicate the onset of each stimulus. However, keep
                   in mind that the 1st column of this matrix doesn't necessary mean the
                   first stimulus position (more on this below).
  'framedesign' - 1 x 25 cell vector for the 25 stimulus positions (order is left to right,
                  then top to bottom); for each element in this cell vector, each row
                  indicates the sequence of faces shown (7x95=665) on a given trial.
                  Multiple rows means that a stimulus position was presented multiple
                  times in the run.
  'classorder' - 1 x 25 indicating the numbering of the stimuli.
                 For example, [5 2 19 ...] indicates that the 5th stimulus (upper-right)
                 is deemed to be the "first" stimulus. Thus, if you do:
                   classorder(find(trialpattern(4,:)))
                 This tells you which stimulus position was presented on the 4th trial.
  'onpattern' - 1 x frames. This indicates the stimulation pattern for each trial.
  'frameorder' - 3 x frames. The first row tells you which face was presented on each of
                 the frames in the experiment.
  'digitrecord' - 1 x 3 cell. The first element is 1 x frames and indicates the digits
                  that were presented during the experiment.



# Instruction for experimenter



# Instructions for subjects

* Subject should maintain fixation on the digits throughout the entire run. This includes the very beginning and very end of the run.

* During the digit task, they should press a button whenever the digit is the same as the previous one. It is possible to get the same digit three times in a row (and so they should press the button twice in this case). Subjects should respond quickly and accurately.

* During the face task, they should press a button whenever the person is the same as the previous one. Each trial always consists of 4 faces. Sometimes there are blank trials, and in these cases, just sit and wait until the next trial. It is possible that there is no button to be pressed within a given trial. It is also possible that there are multiple button presses within a trial. Respond quickly and accurately.

* The same task is performed throughout an entire run. Each run is about 5 minutes.

* There are 12 runs in total, and the experimenter will tell you which task to perform before each run. The tasks will alternate.
