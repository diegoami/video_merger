
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import ffmpy
INPUT_FILE='/media/diego/one_touch/videos/PLNP_nRm4k4jc1yxjDO_pR4-v5_2pVRZwT/1_mlIZyNklCpY'
OUTPUT_FILE='out_2.mp4'
RAW_FILE= 'raw.h264'
# ffmpeg -i input.mkv -filter:v "setpts=PTS/60" output.mkv


import ffmpy
#ff = ffmpy.FFmpeg(
#     inputs={INPUT_FILE: None},
#     outputs={OUTPUT_FILE: '-filter:v "setpts=PTS/60"'}
#)
#
#
# ff.run()
# ffmpeg -i input.mp4 -map 0:v -c:v copy -bsf:v h264_mp4toannexb raw.h264


# ffmpeg -fflags +genpts -r 30 -i raw.h264 -c:v copy output.mp4
ff = ffmpy.FFmpeg(
     inputs={INPUT_FILE: None},
     outputs={RAW_FILE: '-an -map 0:v -c:v copy -bsf:v h264_mp4toannexb '}
)
ff.run()
ff = ffmpy.FFmpeg(
     inputs={RAW_FILE: '-fflags +genpts -r 180'},
     outputs={OUTPUT_FILE: '-c:v copy'}
)
ff.run()

# Concatenate: https://stackoverflow.com/questions/7333232/how-to-concatenate-two-mp4-files-using-ffmpeg