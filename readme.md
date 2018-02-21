## requirements
- Python3
- The modules listed in requirements.txt
- A good healthy internet connection
- ffmpeg in your path

## assumptions (!important)
- WAVE files must be 16 bit, stereo, 44.1kHz
- Include the raw text of the script in the root folder as a .txt file called script.txt

## installation
- `pip3 install requirements.txt`

## running:
Soon this will all be one nice command, but for now, nope.
- Make sure you get json formatted API credentials from google cloud.
- set the CREDENTIALS variable in STT-safe.py to your json formatted api key
- You will need to partition your audio into segments (because google cloud has an upper limit to the length of speech it can transcribe)
  - do so by going `./segmentize PATH/TO/YOUR/WAVE/FILE.wav`
    - note you may need to `chmod 744 segmentize` to give it executable permissions.
    - further note that you need ffmpeg in your path to run segmentize.
- transcribe speech to text by running `python3 STT-safe.py`
- This should have made a new .csv called `transcript.csv` in root. Your job is not yet done, young traveller! You must next associate [script directions] from Michael with the transcription.
- Type `python3 transcriptmatch.py`
- A new .csv called `instructions.csv` has been generated in root.

---
- (SOON BUT NOT NOW) You will be able to simply type `python3 main.py path/to/speech.wav path/to/script.txt`



