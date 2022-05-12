Sphinx and Autodoc
==================

A Fresh Installation
--------------------

The following instructions explain how to use Sphinx and restructured text files to generate beautiful docs without lifting a finger (except to type, you will need to do that).

Sphinx is a Python package, so you'll need to have Python3 installed on your system. This is simple to do, just download it from https://www.python.org/downloads/.
We then need to install Sphinx. The best way to do this is via pip (the Python package manager), inside a virtual environment. This helps keep installations clean
and free from dependency clashes etc. If you care as deeply about proper package installation as I do, then refer to the next section on virtual environment installation,
but if not, skip to the section after.

Installing a Virtual environment
################################

Virtual environments are just small, local python installations within your pc. When you create one and activate it, your code will install packages to this local version,
and this will be used to run your code. It stop issues that occur when pythonCodeA.py runs TensorFlow v.X, while pythonCodeB.py runs TensorFlow v.Y, and you don't want 
to have to keep uninstalling and reinstalling different package versions.

We do this installation from the command line. On a Unix machine (Linux, MAC OS, etc.) go to your search bar and search 'Terminal'. Open this up. If you're using Windows,
type 'cmd' into your search bar and open up a command line.

Windows
*******

With your cmd open, navigate to a directory where you want to install the virtualenvironment folder, such as Documents, eg: ::
    
    cd C://../Documents/MyCode/venvs/

and type: ::

    pip install virtualenv
    virtualenv -p=python3 docsenv

where docsenv is the name of the environment - you can name it whatever you want (but don't include spaces).
Finally, activate your virtual environment by typing: ::

    docsenv/Scripts/activate 

but replace docsenv with whatever name you used.

Unix (Linux, MAC, etc.)
***********************

With your terminal open, navigate to a directory where you want to install the virtualenvironment folder, such as Documents, eg: ::

    cd .../Documents/MyCode/venvs/

and type: ::

    pip install virtualenv
    virtualenv -p=python3 docsenv

where docsenv is the name of the environment - you can name it whatever you want (but don't include spaces).
Finally, activate your virtual environment by typing: ::

    source docsenv/bin/activate

but replace docsenv with whatever name you used.

Anaconda
********

You can also do this with Anaconda. See the Anaconda website for more details and installation instructions.

Back To Sphinx
**************

Now, with your virtualenvironment installed and activated (or not if you're a rebel), install Sphinx via pip: ::

    pip install sphinx sphinx-rtd-theme sphinx-js

And let this complete. Congrats, you have Sphinx installed!

A Fresh Sphinx Project
######################

You can initialise a new Sphinx project by running: ::

    sphinx-quickstart

from within a terminal, where you have navigated to your desired installation directory (see instructions above about finding an appropriate terminal for your system).

This will present some quickstart options to initialise your project, such as project name, author, etc. When asked about separate build and source directories,
I'd suggest opting for separating them, to make things clearer. Type into the terminal to fill these out. Once this is done, the necessary folders will be created 
in your root directory. Depending on the option you chose in quickstart, this will create a build dir, a source dir, and a couple of Makefiles.

Inside source, there are some .rst files which you can edit. Inside build, there are html files which will be updated when you make and apply changes.

To make and apply changes, from inside the same terminal as previously, run: ::

    sphinx-build -b html source build

This command is broken down into: ::

    sphinx-build -b <build-type> <source-dir> <build-dir>

as there are other options available for build-type (such as latex, pdf, etc.) and your source and build directories may differ if your source code is elsewhere.
If your build and source dirs are within the path of your makefile (i.e you did the standard initialisation process and directory structure looks like): ::

    root
    |___makefile 
    |___make.bat 
    |___source/
        |___<...>.rst
    |___build/
        |___<...>.html

Then you can build your project by simply running: ::

    make html

Using the ReadTheDocs Theme 
###########################

As a default, Sphinx uses the Alabaster theme. The most common Sphinx theme is ReadTheDocs (eg. https://sphinx-rtd-theme.readthedocs.io/en/stable/configuring.html). 
To configure your project to use this theme instead, open on the Python file in source/conf.py using any text or code editor. 

On line 17 (approx), add: ::

    import sphinx_rtd_theme

On line 32 (approx) change extensions to: ::

    extensions = [
        'sphinx_rtd_theme'
    ]

And finally, on line 50 (approx), change html_theme to: ::

    html_theme = 'sphinx_rtd_theme'

And rebuild your project! Sometimes Sphinx can get stuck updating the theme, so try navigating up a directory, 
re-navigating to the folder, and building a couple of times until it updates. Open and close the page in your browser
in case the browser has cached the static files.

Autodocumenting
###############

Sphinx allows you to manually edit the .rst files that are compiled into your html pages (as I have here). It is very likely that you
will have to do at least some of this, to add a paragraph saying what your code is, etc.
However, Sphinx also provides tools to auto-generate functional documentation too, which is what we shall cover here.

This guide assumes you're documenting either Python or Javascript code. For alternatives email alex.grogan@xpsy.ox.ac.uk and he'll hack a fix together for you.

Sphinx can extract the docstrings from code blocks and format them into digestable documentation. The difference between docstrings and normal comments is that 
a docstring gives information about a high-level structure. For example, this may be a module, a class, a function, etc.
On the other hand, comments describe what is happening line-by-line, and requires context (i.e the code itself) to be useful for another person to read and understand.
A docstring for python looks like the following: ::

    def someFunction(arg1, arg2):
        """Performs some transformation on the args

        :param arg1: A description of the first arg
        :type arg1: float
        :param arg2: A description of the second arg
        :type arg2: float
        :return: The transformation of the args
        :rtype: float
        """

    ...

    return someData

The specific format of the docstring can vary. The format above works well with Sphinx, and in fact was generated using the python docstring generator plugin
for Visual Studio Code. Similarly, Google recommend a slight variation that makes it slightly more readable within the code, but less so to Autodoc. This can 
be found within the Google styleguide for Python: https://google.github.io/styleguide/pyguide.html

Sphinx naturally works with Python, however, I have made an interpreter for Javascript. The current build of this expects you to use Python docstrings, but 
I'm working on interpreting JS docstrings too, so please follow this repo and the Sphinx4JS repo (https://github.com/agrogan97/Sphinx4JS) to keep up to date with 
changes!

Auto-documenting JS 
*******************

Add docstrings to your code using the Python structure. For example, a JS function with Python docstring would look like: ::

    function someFunction(arg1, arg2) {
        /*Performs some transformation on the args

        :param arg1: A description of the first arg
        :type arg1: float
        :param arg2: A description of the second arg
        :type arg2: float
        :return: The transformation of the args
        :rtype: float

        */

        return someData;
    };

Next, download the Sphinx4JS code from the repo at https://github.com/agrogan97/Sphinx4JS. The src file for this is called `parseJS.py`. This should be stored in the 
root directory of your documentation, alongside the Makefile. Your JS source code can be anywhere on your system, as parseJS.py will take the source directory as a
command-line input. Thus, for src code at local directory code/js/, you would run: ::

    python parseJS.py code/js/ -v 

A code dir with this structure is included within this repo. A single JS file can be found at `code/src/functions.js`. By running the python command above, Sphinx4JS
will translate your JS docstrings into Python, and store them in a local repo called parsedPython. This will be the source directory that Sphinx reads from.
Before we make the autodocs, we need to tell Sphinx where to find our js source code. To do this, open up `source/conf.py`. Underneath the imports, add: ::

    import sys
    sys.path.append('parsedPython')

And now at long last, we can autodocument our code! For each module in parsedPython (where one module is one file), add the 
following to an RST file: ::

    .. automodule:: <filename>
        :members:
        :undoc-members:

replacing filename with the name of a file in `parsedPython`.

For example, using `code/js/functions.js`, we can add the autodoc rst: ::

    .. automodule:: functions
        :members:
        :undoc-members:

.. automodule:: functions
    :members:
    :undoc-members: