<img align="left" src="docs/source/images/small_logo.png">

# Checkpot
## _Final report for GSoC 2018_

**Student:** Vlad Florea

**Organization:** [The Honeynet Project](https://www.honeynet.org/)

#### Relevant links:

- https://github.com/honeynet/checkpot - the new official repository

- https://github.com/vladalexgit/checkpot - development repository, here you can see how the app progressed start to finish by looking at the commit history

#

## Introduction:

Checkpot is a honeypot checker (the first of its kind from my knowledge): a tool meant to detect mistakes in the configuration of honeypots, mistakes that a security researcher could then easily fix before deploying the honeypot in a production environment, in order to avoid detection by the bad guys.

This tool is aimed at security researchers who wish to make sure their honeypots are properly set up so they can be as hard to detect as possible and attract high-quality traffic. Thus it benefits the security industry by making sure all researchers have access to meaningful data so they can develop better security tools to help protect everyone from emerging threats.

According to recent studies, honeypots using default or incorrect settings are surprisingly widespread all across the internet so I consider Checkpot to be very relevant in current times.


## What was done during GSoC 2018:

I have developed this tool from scratch during GSoC 2018. Full commit history so you can see the evolution of the app and how it progressed from zero to hero can be found here: https://github.com/vladalexgit/checkpot/commits/master

I ended up developing and delivering all the following:

- A python framework built specifically as a test platform for honeypots. Tests are based on the strategy design pattern (http://checkpot.readthedocs.io/en/latest/test_platform_description.html), writing a new test is as easy as extending the Test class and overriding a method. Checkpot's framework does all the heavy lifting behind the scenes: takes care of scanning (and then provides the necessary data through various wrappers with everything available at just the call of one method), displays results, calculates stats, generates documentation, etc. This way new tests can be developed and added fast and easy so the app can remain relevant with the security industry evolving at such a rapid pace

- 12 different types of tests, using the above framework, providing detection of default configurations on 16 different honeypots (https://github.com/vladalexgit/checkpot/tree/master/tests)

- An automated testing system based on docker, which works seamlessly with continuous integration systems (like TravisCI), running a set of honeypots inside docker containers and executing tests against them to verify the functionality of Checkpot commit by commit.

- Documentation site (http://checkpot.readthedocs.io), generated using Sphinx and hosted on readthedocs.org, containing information about the structure of the app, guides for contributors, suggested actions for each type of test, and of course documentation for each class and method to help developers extend features and fix problems as fast as possible.

During the development of Checkpot, I also had a lot of interactions with the open-source community out of which the most notable would be the following:

- In order to get ideas for more detection methods and find out what features an expert in this domain would expect from an app like mine, I have been communicating with authors of honeypots like Lukas Rist (author of Glastopf, Conpot, and others) and Michel Oosterhof (author of Cowrie).

- I came across a bug in Conpot which I have reported and the developers are working to get fixed for a later version: https://github.com/mushorg/conpot/issues/384

## What is left to do:

- First of all, more tests should be added, usefulness of the app will increase proportionally with the number of tests, as more honeypots are supported. This is quite a time-consuming task so it would be ideal to build a community of contributing developers around the project.

- Although I have done extensive testing using different environments and conditions plus also developed the automated testing framework, I am sure however that some bugs remain somewhere in the app, which will surface at some point and will need to be fixed.

- A more challenging task would be the research and development of new testing/detection methods using more efficient techniques. I have done some research in this area during the project but I was not able to find more efficient methods.


## What I learned and closing remarks:

GSoC has been an enriching experience for me. I have learned plenty of things and had a lot of fun this summer developing Checkpot.

Before I applied for this project I didn't know much about honeypot technologies. I have always been passionate about the field of computer security and thought this would be the perfect project for me. So I have done a lot of research to get up to speed on the subject in order to submit a strong project proposal and, in the end, I actually got accepted! This made me very happy but I knew however that I had no easy task ahead.

I have come across many challenges during the design of the app:

- Some were technology related: creating the class structure, making sure I get everything right from the beginning so I won't have to make changes later on and ensuring the project will be as modular, extensible and easy to maintain as possible in the future.

- Others were related to ethics: making sure the checker would only detect issues that the researchers can easily fix, thus helping them develop better security tech for everybody by having access to high-quality data and not building an "all in one" honeypot detector to be used by the bad guys and cause harm.

I am super grateful I had the opportunity to learn the ins and outs of this domain from world-class experts. 

I would like to give a huge "Thank You!" to my mentor, Marcin Szymankiewicz, who was always there to help me with code reviews, advice, etc. 24/7 and without which the creation of Checkpot would have never been possible. I would also like to thank everybody inside and outside The Honeynet Project for all their help and advice regarding this project. I hope this tool will be a useful addition to the open-source community. It might be the end of GSoC 2018 but, for Checkpot this is only the beginning!

