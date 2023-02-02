
# See PyCharm help at https://www.jetbrains.com/help/pycharm/
import ffmpy
INPUT_FILE='/media/diego/one_touch/videos/PLNP_nRm4k4jc1yxjDO_pR4-v5_2pVRZwT/1_mlIZyNklCpY'
OUTPUT_FILE='out.mp4'

# ffmpeg -i input.mkv -filter:v "setpts=PTS/60" output.mkv


import ffmpy
ff = ffmpy.FFmpeg(
     inputs={INPUT_FILE: None},
     outputs={OUTPUT_FILE: '-filter:v "setpts=PTS/60"'}
)
ff.run()