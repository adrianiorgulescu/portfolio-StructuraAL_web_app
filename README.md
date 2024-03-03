# StructurAL
#### Video Demo: https://youtu.be/FXfncJuL_cA
#### Description:

Greetings!

Welcome to my CS50 final project!

The aim of this project is to create an online (web-based) tool that can perform a number of structural engineering calculations. For the purpose of this project, I will keep the number of functions limited to one (1), in order to reduce the volume of work, but I am planning to update the code in order to add more calculations. The calculation carried out is for a reinforced concrete beam.
The project is developed using the Python language and the Flask framework for developing web applications. More details about the code are given in the 'The code' section of this file.
Why am I doing this project and what is its use?
I probably need to mention that I am a structural engineer and I use this kind of tools all the time. It is either proper software packages (commercial tools produced by others) or MS Excel spreadsheets produced by me. But now that I took CS50 it is time to jump from the MS Excel spreadsheets to a more developed web-based tool.
The use of this tool is to allow an engineer perform simple calculations during the structural design process. There will be an input of certain physical parameters and there will be an output from the application with the results of the calculations.
The tool will be based on the current regulations used in the UK for structural engineering calculations (the Eurocode package).

## How to use the tool

Create an account and log-in.

Once logged-in you will be taken to the index page, where you can select a calculation you wish to perform from the list of calculations available. Please note that, as described in the introduction, only one calculation is available at the current stage, which is the "reinfroced concrete beam calculation".

Once you've selected the calculation you wish to perform, navigate through the pages using the next button and ensure to provide information at all the input fields as required by the page. Please note that at the current stage no form validation has been set in place, as such the user will need to carefully read all the notes and ensure all the input fields are correctly filled-in.

On the first calculation page the user will be asked for input for the beam geometry: length, section width, section depth. Only beams with a rectangular cross section and with a simply supported static scheme are accepted by the current version of the tool.
On the second calculation page the user is asked for input relating to the loads present on the beam. The user will have to create additional rows in the table with the buttons given in order to be able to add all the loads required. Clear indications are given on the page as to how the information needs to be inserted. If the information is not introduced correctly an error page will be shown.
On the third calculation page the user is requested input relating to the material properties and further geometrical properties (i.e. cover to reinforcement).
On the final page a summary of all the information introduced is presented. The results of the static and reinforcement requirement calculations which were carried out in the background are also presented. The user will have to provide the tension reinforcement to the beam in order to be equal or greater than the required reinforcement. A input field is provided in order for the user to select the diameter and number of bars. If the tension reinformcement area selected is sufficient, a PASS message will appear. Similarly, for the shear reinforcement.
Once all the calculations have been performed, there is an option to save the output in a pdf file.

## Features

- Reinforced concrete beam design in accordance with the Eurocode regulation.

## Getting started

- Make sure you have Python 3 installed on your computer.
- Clone this repository to your local machine.
- Install the Python packages as indicated in the requriements.txt file
- Run the application in your terminal by executing the following command: flask run

## The code

The application is developed using the Flask framework, using Python, HTML, CSS and JavaScript.
What the individual files/folders do/contain:
- static folder - this folder contains the static files required by the web pages; A styles file is provided for the CSS code and a JavaScript file is provided which contains the JavaScript code required by some of the pages.
- templates folder - this folder contains all the templates for the individual web pages used by the application.
- app.py - this is where all the python code for running the Flask application is written.
- concrete_class_t.csv - is a file containing information about the concrete classes - this is used by the application; the information is uploaded in the database.
- helpers.py - this is a python file containing all the helper functions as required by the application.
- Readme.md - the current file.
- requirements.txt - contains all the requirements for runnign the application.
- structural.db - repesents the database for the project, where all the information is saved for the calculations performed.

For the conversion of the html code to the pdf file (when exporting the calculation results) the tool html2pdf.js is used (https://ekoopmans.github.io/html2pdf.js/). The script is referenced in the code on the A-RC-beam-3.html page.

## Author

This project was created by Adrian Iorgulescu as part of the CS50 Final Project.

## Contribute

If you'd like to modify this project, feel free to do so as you see fit. I am sure that the game can have more features or have its usability improved.

## Acknowledgments

I'd like to thank the CS50 team for the great work they are doing, and in particular to Professor David J. Malan for teaching us the art of programming.


