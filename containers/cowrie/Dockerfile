FROM cowrie/cowrie

# enable telnet service
# RUN sed -i '/# Enable Telnet support, disabled by default/!b;n;ceenabled = true' /cowrie/cowrie-git/cowrie.cfg.dist

RUN echo "[telnet]" > /cowrie/cowrie-git/cowrie.cfg
RUN echo "enabled = true" >> /cowrie/cowrie-git/cowrie.cfg
