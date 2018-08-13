<img align="left" src="docs/source/images/small_logo.png">

# Checkpot

Honeypot Checker

[![Build Status](https://travis-ci.org/vladalexgit/checkpot.svg?branch=master)](https://travis-ci.org/vladalexgit/checkpot)
[![Documentation Status](https://readthedocs.org/projects/checkpot/badge/?version=latest)](http://checkpot.readthedocs.io/en/latest/?badge=latest)

<br />
<br />

## Introduction

Checkpot is a honeypot checker: a tool meant to detect mistakes in the configuration of honeypots. It is aimed at security researchers who wish to check that their honeypots are properly set up, so they can be as hard to detect as possible and attract high-quality traffic. According to recent studies, honeypots using default or incorrect settings are surprisingly wide spread all over the internet so we consider Checkpot to be very relevant.

 _“Many researchers fail deploying honeypots that are easily detectable. There are trivial mistakes people can make when deploying a honeypot like leaving the default settings or templates. On the other hand there are some non-direct indicators of a honeypot including but not limited to running both Windows and Linux services on the same box or having two different ssh servers listening on the same IP. The goal of this project would be to create a simple and open source honeypot detection tool that would scan an IP looking for any traces of a honeypot and create a report with findings and their severity. Using this tool a researcher can scan their system before putting it online or in production and based on the report perform the necessary tuning.”_ - [Honeynet GSoC 2018 project proposal](https://www.honeynet.org/gsoc2018/ideas#honeypot-detection)

#### _Notice:_

We don't want under any circumstances to make things easier for the bad guys, on the contrary, we wish to give them a hard time staying hidden by helping all researchers set up their honeypots properly.
 
All our tests are based on default settings or bugs that can be changed/avoided easily by security researchers. We **NEVER** publish tests that could expose honeypots when an easy fix for them is not available!

## Disclaimer

##### As this software is PROVIDED WITH ABSOLUTELY NO WARRANTY OF ANY KIND,
##### YOU USE THIS SOFTWARE AT YOUR OWN RISK!

##### By using this tool YOU TAKE FULL LEGAL RESPONSIBILITY FOR ANY POSSIBLE OUTCOME!
 
Keep in mind that this tool is based on port scanning and interacts with services on the target system in most cases. Even a simple port scan can be illegal in some jurisdictions. Please consult all laws that apply to your use case and make sure you understand exactly how the app works before you use it.
 
Our recommendation to make sure you stay out of trouble is to only scan systems that you own or systems whose owner has legally authorized you to scan (you can find an example [here](https://www.owasp.org/index.php/Authorization_form)).

## _Temporary Notice_

_This tool is still in very early stages of development. Please keep this in mind when using it and contact the authors if you notice any problems (you can find all contact info at the bottom of this page)._

## How to install Checkpot

   1. Read the Disclaimer above very carefully. Remember: USE CHECKPOT AT YOUR OWN RISK!
   2. If you do not understand the disclaimer stop now!
   3. Clone this repository locally:
   
        `git clone https://www.github.com/honeynet/checkpot.git`
   
   4. Install `python3` (recommended version 3.5 or greater) and `pip` using apt-get or tools like virtualenv or conda
   
   5. Install `mercurial` using apt-get (or your distribution's default package manager). Mercurial is required for the download of some dependencies during the next step.
   
   6. Install all required packages from requirements.txt:
   
        `pip install -r requirements.txt`
   
   7. _Optional:_ If you wish to run the automated tests or use the containers framework for development purposes install docker.io:
   
        `sudo apt-get install docker.io`

## How to use Checkpot

Run `python checkpot.py` without any arguments to see all available commands

A typical usage example would be: `python checkpot.py -t <IP> -l 3` 

## Documentation

You can read the documentation [here](https://checkpot.readthedocs.io/en/master/).

If you still have doubts on how something works you can contact us anytime on the [official Honeynet slack channel](https://honeynetpublic.slack.com/) or open an issue here on github. We are here to help.

## Contributions

We welcome bug reports, suggestions for new features, new tests or improvements for existing tests.
 
We always strive to make Checkpot as modular and easy to understand as possible so everyone can contribute.
 
If you are a honeypot developer you can help your users set it up properly by adding tests for your honeypot.

A guide for contributors can be found [here](checkpot.readthedocs.io/en/latest/guides_for_contributors.html).

## Contact

If you still have doubts on how something works, you are facing any issues or have any suggestions you can contact us anytime on the [official Honeynet slack channel](https://gsoc-slack.honeynet.org/) or open an issue here on github. We are here to help!

##

Proudly developed during [Google Summer of Code 2018](https://summerofcode.withgoogle.com/projects/#4742143558549504) for [The Honeynet Project](https://www.honeynet.org/).
