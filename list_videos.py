import urllib.error

import os

import os
import yaml
import time
import ffmpy
import argparse
from os import listdir
from os.path import isfile, join
from ffprobe import FFProbe

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config')  # option that takes a value
    args = parser.parse_args()
    if args.config == None:
        print("required argument --config <config>")
    else:
        with open(args.config, 'r') as confhandle:
            conf_info  = yaml.safe_load(confhandle)
            video_dir = conf_info["video_dir"]
            playlist_id = conf_info["playlist_id"]
            max_seg_width = conf_info["max_seg_width"]
            playl_dir = os.path.join(video_dir, playlist_id)

            onlyfiles = [f for f in listdir(playl_dir ) if isfile(join(playl_dir, f))]
            sfiles = sorted(onlyfiles, key=lambda x: int(x.split('_')[0]), reverse=False)
            print(sfiles)
            segs, run_length = [[]], 0
            seg_index = 0
            for sfile in sfiles:
                segs[seg_index].append(sfile)
                full_file = os.path.join(playl_dir, sfile)
                metadata = FFProbe(full_file)

                for stream in metadata.streams:
                    if stream.is_video():
                        print('{} has duration in seconds: {}'.format(sfile, stream.duration_seconds()))
                        run_length += stream.duration_seconds()
                        if run_length > max_seg_width:
                            segs.append([])
                            seg_index += 1
                            run_length = 0
            print(segs)