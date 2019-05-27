# Udacity Item Catalog project: -
### By Ahmed Alhawsawi
## ReadMe.md 

### Introduction
This project is the second project for those who enrolled in Full-Stack Web Developer Nanodegree program which is introduced by Udacity platform. The aim of this project is to build the website from scratch. This website is combined the skills of building database, working with CRUD (Create, Read, Update, and Delete) operations, and applying Flak framwork in python with the integration of third party as authentication and authorization. 

### Requirements:  
- [Python 2.7, 3.5](https://www.python.org/) or latest version of Python programming language.
- [VartualBox](https://www.virtualbox.org/) the software that runs the Virtual Machine (VM) environment locally in the Operating System (OS).
- [Vagrant](https://www.vagrantup.com/) the software that lunches and configures the virtual machine in your computer.
- [Git](https://www.git-scm.com/) a free and open source Unix-style terminal. 

### How to get to the project: 
Downloading [VartualBox](https://www.virtualbox.org/) and [vagrant](https://www.vagrantup.com/) from their websites and set all the requirements for running the virtual machine. Then, installing [Git](https://www.git-scm.com/) to operate the virtual machine environment. Finally, clone or download the [Vagrant VM configuration file](https://github.com/udacity/fullstack-nanodegree-vm).

### Runing the virtual machine
- $ vagrant up
- $ vagrant ssh
- $ cd  /vagrant/catalog 
- $ pip  install  -r  requirements.txt 
- $ python database_setup.py
- $ python lotofmenu.py
- $ python application.py
- Then Accessing and testing the application by visiting http://localhost:8000 locally
