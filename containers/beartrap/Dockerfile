FROM ruby

RUN git clone https://github.com/chrisbdaemon/beartrap.git
RUN gem install getopt

CMD cd beartrap && ruby bear_trap.rb -c config.yml
