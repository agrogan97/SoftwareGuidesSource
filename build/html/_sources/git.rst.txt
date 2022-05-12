Git Tutorial
############

Cheatsheet link!:: 
    
    PDF: https://training.github.com/downloads/github-git-cheat-sheet.pdf
    Visual: https://ndpsoftware.com/git-cheatsheet.html

First Installation
------------------

Download the appropriate version of git for your system. See https://git-scm.com/downloads for operating-system specifics.

With git installed locally, open up a terminal (or a git bash shell if using Windows). Type::

    git help git 

This will open up the Github manual in a browser window (handy for referencing) and also confirm successful installation. Git is intrinsically a version control tool, with
it's own Command Line Interface (CLI). Github is a an organisation that hosts remote repositories on their own servers that users can access. Therefore you can use 
git without using github, but can't use github (for version control) without using git!

Alternatives to Github do exist, for instance Gitlab (https://about.gitlab.com/) which has some excellent features, and allows users to host their own private 
repository servers.

With your terminal open, run the following commands to let git know who you are: ::

    git config --global user.name "[name]"
    git config --global user.email "[email address]"

replacing [name] and [email address] with your own details, but keeping the speech marks.

Now, see the sections below to find out how to do what you need to do!

I Want To....
--------------

Find the section below relating to what you want to achieve with git.

Create a local repo for my code
===============================

Navigate to your source code root directory and run::

    git init 

To initialise a new repo. This is a hidden folder, and may not appear in file explorer or equivalent. It is common to also initialise a project with a 
README.md file, and a .gitignore file. These can be created from the terminal with: ::

    touch README.md 
    touch .gitignore

making sure to include the full stop before gitignore. For Windows users, create these files manually or using Windows-specific commands.

To add everything to your local repo, regardless of project stage, complete the following steps:

Run::

    git add .

This wil add everything to the git staging area. We can see more details about what has been staged and not by running::

    git status

Next, run::

    git commit -m "commit message"

This will commit everything in the staging area to the local repo. Note that this has nothing to do with Github, so far this is entirely on your local machine!
The -m flag appends a commit message to the command. You can include a short, custom message explaining what changes you have made here, within the speech marks. If you ran 
this command without that flag, git would open a VIM window, where you are expected to type out and enter a message.

Store Code on Github 
====================

Firstly, make sure you have a Github account. You do this simply from https://github.com/.

The first thing to do is create a new Github repo to store your code, or copy your local repo to. Do this from the green 'new' button on the left-hand side toolbar and follow
the instructions to name it. This will create a unique URL to your

