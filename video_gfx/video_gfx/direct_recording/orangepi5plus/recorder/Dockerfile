FROM python:3.10

ARG PORT=9003

RUN apt update
RUN apt -y upgrade
RUN apt -y install ffmpeg

WORKDIR /usr/src/app
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY . .

EXPOSE $PORT



# Run the ffmpeg command
CMD sleep 9 && ffmpeg -y -f x11grab -video_size 1920x1080 -r 50 -i :0 -t 5 recording.mp4 
# CMD sleep 7 && \
# -framerate 25
    # ffmpeg -y -video_size 1920x1080  -f x11grab -i :0.0 -q:v 0 -y raw_output.mkv && \
    # ffmpeg -i raw_output.mkv -c:v libx264 output.mp4
    #  -t 5 -c:v libx264rgb -crf 0 -r 50 -preset ultrafast -color_range 2 recording.mp4 
# & sleep 5 && echo "q" > /proc/1/fd/0
# CMD ["ffmpeg", "-y", "-f", "x11grab", "-draw_mouse", "0", "-video_size", "VIDEO_SIZE", "-r", "FRAME_RATE", "-i", "chromium:0+nomouse", "-codec:v", "CODEC", "-preset", "PRESET", "-tune", "zerolatency", "-pix_fmt", "yuv420p", "-color_range", "1", "-crf", "13", "recording.mp4"]
# CMD ["python3", "main.py"]
