import subprocess
import sys, os
import STT
import transcriptmatch
from pprint import pprint as p


def check_required_files():
    root = os.listdir(".")
    api_key = os.listdir("api_key")
    print(api_key)
    if ("script.txt") not in root:
        print("😮  missing script.txt file!\n    👉  copy a script as a plaintext file and save it as 'script.txt' in the root directory.")
        exit()
    else:
        print("✓ found script.txt")
    for f in api_key:
        print("searching",f)
        if (".json") in f:
            print("✓ found API key looking object")
            return
            
    print("😮  missing json formatted API key")
    exit()

def main():
    if len(sys.argv) > 1:
        if ".wav" in sys.argv[1]:
            check_required_files()
            print("Segmentizing",sys.argv[1])
            subprocess.call(['ffmpeg -i $1 -f segment -segment_time 10 -c copy segments/$1_out%03d.wav',sys.argv[1]])
            STT.main()
            transcriptmatch.main()


        else:
            print(sys.argv[1],"is not a wave file. (Remember to include the .wav extension!)")
    elif len(sys.argv) == 1:
        print("Supply a wave file as an argument")

main()