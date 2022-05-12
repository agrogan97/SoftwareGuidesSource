"""
Author: Alex Grogan (2022)
Institution: University of Oxford, Department of Experimental Psychology

Summary:
    - Tool for auto-documenting Javascript using the Sphinx framework.
    - Initially, will convert javascript docstrings into Python docstrings and use that to auto-generate Sphinx documentation
    - This will be extended into auto-creating code dependency trees, and so on
    - For feature requests, please contact the author, or raise an issue in Github
    - For bug reports, please contact the author, or raise an issue in Github

Usage:
    - This module acts as the sole entrypoint. To run the code, run the following from a terminal with Python3.* installed:

        python parseJS.py <JSSourceDir> -v

Flags:
    -v : Verbose mode

"""

import sys
import os
import re

def asciiArtIntro(verbose=True):

    if verbose:

        print("""
         ______        _     _               
        / _____)      | |   (_)              
        ( (____  ____ | |__  _ ____  _   _   
        \____ \|  _ \|  _ \| |  _ \( \ / )  
        _____) ) |_| | | | | | | | |) X (   
        (______/|  __/|_| |_|_|_| |_(_/ \_)  
                |_|                          
           ___               _______ ______ 
          / __)             (_______) _____)
        _| |__ ___   ____        _ ( (____  
       (_   __) _ \ / ___)   _  | | \____ \ 
        | | | |_| | |      | |_| | _____) )
        |_|  \___/|_|       \___/ (______/ 
                                            
        """)

def getSourceDir():
    """Read CLI and retrive the source directory of the JavaScript files to be documented

    :return: source directory filepath
    :rtype: string
    """

    # TODO Handle exceptions

    if sys.argv[1] == '.':
        return ''
    else:
    # Return the second CL argument
        return sys.argv[1]

def createParsedPythonDir():
    """Create a folder in the root directory called parsedPython, to store the python files generated by this process

    :return: None
    :rtype: None
    """

    if os.path.exists("parsedPython"):
        return None
    else:
        os.mkdir("parsedPython")

def generateDummyPython2(jsTxt):
    """Take in javascript from a single file and convert the JS docstrings into Python docstrings

    :param jsTxt: The javascript, as a line-by-line list
    :type jsTxt: array-like of strings
    :return: list of line-by-line Python docstrings, including function names and params
    :rtype: array-like of strings
    """

    numFunctions = 0

    # All of our docstrings
    pythonDocstrings = []

    withinDs = False

    for line in jsTxt:
        # Check if it is of the structure: function ...() {
        if line.startswith('function') and line.endswith('\n'):
            # This is a function declaration line, so take what we need using regex:
            # function name
            fname = re.findall('[\b\(\)(, \s)]([a-zA-Z0-9]+)', line)[0]
            fargs = re.findall('[\b\(\)(, \s)]([a-zA-Z0-9]+)', line)[1:]
            pythonDocstring = ('def %s(' % fname)
            for x in fargs:
                pythonDocstring += x + ','
            pythonDocstring += "):"
            pythonDocstrings.append(pythonDocstring.lstrip().rstrip())
            numFunctions += 1
        # Loop over the docstring
        if (line.lstrip()).startswith('/*') and not withinDs:
            dsStart = re.search('(?<=[\/\*])[\w|\s]+', line).group()
            pythonDocstrings.append("\t" + '"""' + dsStart.lstrip().rstrip())
            withinDs = True
        elif line.endswith('*/\n'):
            dsEnd = line[:-3]
            pythonDocstrings.append("\t" + dsEnd.lstrip().rstrip() + '"""\n')
            # pythonDocstrings.append('\n')
            withinDs = False
        elif withinDs:
            # Remove leading whitespace and ending newline
            pythonDocstrings.append("\t" + line.lstrip().rstrip())

    print("Parsed %d functions from file" % (numFunctions))

    return pythonDocstrings

def generateDummyPython(jsTxt):
    """Take in javascript from a single file and convert the JS docstrings into Python docstrings

    :param jsTxt: The javascript, as a line-by-line list
    :type jsTxt: array-like of strings
    :return: list of line-by-line Python docstrings, including function names and params
    :rtype: array-like of strings
    """

    numFunctions = 0

    # All of our docstrings
    pythonDocstrings = []

    # Track which line number we're on
    lineCount = 0

    for line in jsTxt:
        if 'function' in line:
            currentFunctionLine = lineCount
            # Keep track of how many functions we've got
            numFunctions = numFunctions + 1
            # And get the main part, including the function name and the input params
            # Split by ()
            funcMain = line.split("(")
            # Grab the second part, which will be just the function name text
            funcName = funcMain[0].split(" ")[1]
            print(line)
            # Take the second item in the list, and split by closing brackets ')', then split by spaces
            if len(line) != 0:
                print("full line")
                funcParams = funcMain[1].split(")")[0].split(",")
                # funcParams = re.split("(|,|, |)", funcMain[1])
                # And formulate the python function opener:
                pythonEquivalent = ("def %s(" % (funcName))

                # Need index of last item so we know when to close the brackets
                indexOfLast = funcParams.index(funcParams[-1])
                # Iterate over each of the parameters we got from the substring list
                for entry in funcParams:
                    if funcParams.index(entry) == indexOfLast:
                        pythonEquivalent = pythonEquivalent + entry + "):"
                    else:
                        pythonEquivalent = pythonEquivalent + entry + ", "

                # This leaves us with a string of the function parameters
                newPythonDocstring = pythonEquivalent

                # Will be true when the line we're cuurently iterating over is a doctstring line (i.e we haven't seen '*/' yet)
                trackingFunc = True
            else:
                # Add a newline?
                pass
        
        # Get the next line after our function
        if trackingFunc:
            # Get the start and end indices:
            if '/*' in line:
                # I think this won't work because of how index works - it'll just find the first example from the list, not the current example
                docstringStartIndex = jsTxt[currentFunctionLine:].index(line)
            if '*/' in line:
                docstringEndIndex = jsTxt[currentFunctionLine:].index(line)
                # Got the ending, so we can stop tracking our function:
                trackingFunc = False

                # and then commentText is all the lines between these 2
                commentText = jsTxt[currentFunctionLine:][docstringStartIndex+1:docstringEndIndex]

                # This includes all the leading whitespace for tabs, so we can keep it

                pythonCommentMarker = ' """ '

                newPythonDocstring = newPythonDocstring + "\n" + pythonCommentMarker

                for item in commentText:
                    # TODO: Check this, might encounter problems removing the newline character this way?
                    newPythonDocstring = newPythonDocstring + item

                # Append closing structure
                newPythonDocstring = newPythonDocstring + pythonCommentMarker

                # print(newPythonDocstring)

                # And finally add it to the cumulative list for all functions in the JS file
                pythonDocstrings.append(newPythonDocstring)

        lineCount = lineCount + 1

    print("Converted %d JS functions into python..." % (numFunctions))

    return pythonDocstrings

def saveTxtAsPython(allPython, filename):
    """Save text to disk as python files

    :param allPython: list of python functions and docstrings, line by line in a list
    :type allPython: array-like of strings
    :param filename: the name of the file to be saved to disk
    :type filename: string
    :return: None
    :rtype: None
    """
    filepath = 'parsedPython/' + filename + '.py'
    with open(filepath, 'w') as f:
        for item in allPython:
            f.write("%s\n" % item)

    print("JS written to disk as Python!")

    return None

def handleCLI(inputs):
    """Handle the command-line inputs and option flags

    :param inputs: The optional CLI inputs 
    :type inputs: string
    :return: config dict with the run settings
    :rtype: dict
    """

    CONFIG = {
            "VERBOSE" : False
        }

    if len(inputs) < 2:
        # No additional flags, skip
        return CONFIG

    for flag in inputs[2:]:
        if "-v" in flag:
            CONFIG["VERBOSE"] = True

    return CONFIG

def main():

    CONFIG = handleCLI(sys.argv)

    asciiArtIntro(verbose=CONFIG["VERBOSE"])

    # Get the source dir:
    sourceDir = str(getSourceDir())
    
    # Get list of all js files in the specified dir
    jsFiles = [f for f in os.listdir(sourceDir) if f.endswith('.js')]

    # And iterate over all these files
    for jsf in jsFiles:
        # Load in each file line by line as txt
        with open(sourceDir + jsf) as f:
            jsTxt = f.readlines()
            print("Opened %s" % (jsf))

        # With our js as txt, create a dedicated python dir (or pass if existing)
        createParsedPythonDir()

        # Parse the jsTxt and convert to dummy python
        allPython = generateDummyPython2(jsTxt)

        # And save the new Python dosctrings to disk - using the original filename but replacing it with .py
        saveTxtAsPython(allPython, jsf[:-3])

    print("\nDone! Now run make html to build your Sphinx files.")

    return None

if __name__ == "__main__" : main()