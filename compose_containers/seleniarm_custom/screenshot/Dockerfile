FROM seleniarm/standalone-chromium

USER root

# install fonts
RUN apt-get -qqy update && apt-get install -y fonts-roboto fonts-recommended fonts-liberation fonts-liberation2

# # install openvpn
# RUN apt-get -qqy update && apt-get install -y openvpn openresolv
# RUN wget "https://raw.githubusercontent.com/ProtonVPN/scripts/master/update-resolv-conf.sh" -O "/etc/openvpn/update-resolv-conf"
# RUN chmod +x "/etc/openvpn/update-resolv-conf"

# RUN mkdir -p /dev/net && \
#     mknod /dev/net/tun c 10 200 && \
#     chmod 600 /dev/net/tun && \
#     /etc/init.d/openvpn restart
# RUN echo tun >> /etc/modules
# RUN chmod 666 /dev/net/tun

# COPY config.ovpn config.ovpn
# COPY credentials.txt credentials.txt
# RUN openvpn ./config.ovpn


USER 1200
