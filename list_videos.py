import urllib.error

import os

import yaml
import time
import ffmpy
import argparse
from os import listdir
from os.path import isfile, join
from ffprobe import FFProbe


def build_segs(playl_dir):
    onlyfiles = [f for f in listdir(playl_dir) if isfile(join(playl_dir, f))]
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
    return segs

def save_segs_to_files(playl_dir, playl_out_dir, segs):
    for index, seg in enumerate(segs):
        file_name = f'list{index + 1}.txt'
        full_file_name = os.path.join(playl_out_dir, file_name)
        with open(full_file_name, 'w') as f:
            for file_name_tow in seg:
                full_file_name_tow = os.path.join(playl_dir, file_name_tow)
                f.write(f"file '{full_file_name_tow}'\n")


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
            output_dir = conf_info["output_dir"]
            playl_dir = os.path.join(video_dir, playlist_id)
            list_dir = conf_info["list_dir"]

            playl_out_dir = os.path.join(output_dir, playlist_id)
            os.makedirs(playl_out_dir, exist_ok=True)
            text_out_dir = os.path.join(os.getcwd(), list_dir)
            os.makedirs(text_out_dir, exist_ok=True)

            segs = build_segs(playl_dir)
            save_segs_to_files(playl_dir, text_out_dir, segs)


