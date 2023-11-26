FROM ubuntu:22.04 

ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get -y update && apt-get -y install software-properties-common
RUN add-apt-repository -y ppa:jjriek/rockchip

# Add mesa and rockchip multimedia ppa
RUN add-apt-repository -y ppa:liujianfeng1994/panfork-mesa
RUN add-apt-repository -y ppa:liujianfeng1994/rockchip-multimedia
RUN apt-get -y update && apt-get -y upgrade && apt-get -y dist-upgrade

# Packages for testing GPU performance. Namely glmark2
RUN apt-get update && apt-get install -y mesa-utils libgl1-mesa-glx libgl1-mesa-dri x11-apps libcanberra-gtk* libglfw3-dev libglew-dev
RUN apt-get update && apt-get -y install glmark2

# Install secondary packages
RUN apt-get update && apt-get install -y x11vnc fluxbox wget

# Install Chromium and chromedriver for RK3588 from https://launchpad.net/~liujianfeng1994
RUN apt-get update 
RUN apt-get install -y chromium-browser
RUN apt-get install -y chromium-chromedriver

RUN apt-get update 
RUN apt-get install -y python3.10 python3-pip

COPY ./requirements.txt .

RUN python3 -m pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .

# # Alternative for Chromium and chromedriver. Also runs with HW acceleration
# RUN add-apt-repository ppa:saiarcot895/chromium-beta

# Set the display environment variable
ENV DISPLAY=:0

# Create the VNC password directory
# RUN mkdir -p /root/.vnc/

# Set the VNC password to "current_time"
# RUN x11vnc -storepasswd current_time /root/.vnc/passwd

# Expose VNC port
# EXPOSE 5901

# Start Xorg, x11vnc, and fluxbox
# CMD Xorg :0 -config /etc/X11/xorg.conf -nocursor & \
# CMD    sleep 5 && \
#     DISPLAY=:0 x11vnc -rfbauth /root/.vnc/passwd -forever -shared -bg -rfbport 5901 & \
#     DISPLAY=:0 fluxbox


# CMD while true; do x11vnc -rfbauth /root/.vnc/passwd -forever -shared -rfbport 5901 -display :0; sleep 1; done

# CMD chromium-browser --no-sandbox & \
#     sleep 5 && \
#     x11vnc -display :0 -rfbauth /root/.vnc/passwd -forever -shared -bg -rfbport 5901 


CMD sleep 1 && \ 
    xhost + && \
    python3 main.py 
# CMD chromium-browser --no-sandbox --ignore-gpu-blocklist

