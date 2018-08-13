FROM honeynet/conpot

# Override CMD to run the test configuration ("-f")
# Never use '-f' when running your own honeypots, using defaults will make your honeypot easily detectable!
# The very purpose of checkpot is to prevent this!

CMD ["/usr/local/bin/conpot", "-f", "--template", "default", "--logfile", "/var/log/conpot/conpot.log"]
