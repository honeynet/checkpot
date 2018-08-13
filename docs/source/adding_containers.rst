Adding new containers
=====================

In order to add new containers all you must do is create a new subfolder inside the containers folder, named after the honeypot it is going to represent (the automated testing framework will be referencing the container by the name of this folder later) and add a Dockerfile inside this container with all the build instructions.

Any other files needed for the container e.g: configs, logs, etc. should reside in the same subfolder as the Dockerfile.
