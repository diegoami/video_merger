# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import ffmpy
import argparse
import os
import yaml
from os.path import basename

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config')  # option that takes a value
    args = parser.parse_args()
    if args.config == None:
        print("required argument --config <config>")
    else:
        with open(args.config, 'r') as confhandle:
            conf_info = yaml.safe_load(confhandle)
            video_dir = conf_info["video_dir"]
            acc_video_dir = conf_info["acc_video_dir"]
            playlist_id = conf_info["playlist_id"]
            max_seg_width = conf_info["max_seg_width"]
            output_dir = conf_info["output_dir"]
            playl_dir = os.path.join(video_dir, playlist_id)
            list_dir = conf_info["list_dir"]
            playl_out_dir = os.path.join(output_dir, playlist_id)
            playl_acc_dir = os.path.join(acc_video_dir, playlist_id)
            frames = conf_info["frames"]
            os.makedirs(playl_out_dir, exist_ok=True)
            os.makedirs(playl_acc_dir, exist_ok=True)

    list_files_left = True
    index = 1
    while list_files_left:
        current_file = os.path.join(list_dir, f'list{index}.txt')
        if os.path.isfile(current_file):
            with open(current_file, 'r') as file_list:
                files_left = True
                file_index = 1
                while files_left:
                    file_line = file_list.readline()
                    if file_line:
                        input_file = " ".join(file_line.split()[1:]).replace("'", "")
                        basename_input_file = basename(input_file)
                        intermedfile = os.path.join(playl_acc_dir, f'raw_{basename_input_file}.h264')
                        outputfile = os.path.join(playl_acc_dir, f'{basename_input_file}.mp4')
                        ff = ffmpy.FFmpeg(
                            inputs={input_file: None},
                            outputs={intermedfile: '-an -map 0:v -c:v copy -bsf:v h264_mp4toannexb '}
                        )
                        ff.run()
                        ff = ffmpy.FFmpeg(
                            inputs={intermedfile: f'-fflags +genpts -r {frames}'},
                            outputs={outputfile: '-c:v copy'}
                        )
                        ff.run()
                        file_index += 1
                    else:
                        files_left = False
            index +=1
        else:
            list_files_left = False