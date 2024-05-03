# Capstone Project

A testing app that reads from a CSV file and quizzes the user on the contents of that file.

## Table of Contents

- [Installation](#installation)
- [Educator's Section](#educators-section)
- [Configuration](#configuration)

## Installation

To install the Capstone Project, follow these steps:

1. Clone the repository: `git clone https://github.com/Donnyd88/CIS291.git`
2. Navigate to the project directory "dist" folder.
3. Run Capstone_Project.exe by double-clicking on it.

    Note: This is a 64-bit Windows version.

Alternatively, the Capstone_Project.py file can be run. This requires python to be installed.


## Educator's Section

To access the educator's section, enter the password: `password`.

You'll want to change the default password once you have accessed the educator's section.

If you need to reset the password to default. Delete the config.csv file included. This will cause the file to be recreated with the defaults once the app is run again. The password will now be `password` again.
Note this will reset all the educator's settings.

## Configuration

When entering percentages do not put a decimal unless intended. The app already converts to a percentage.
Also, do not include a `%` sign.

Example:
Input : `90`
That will create a threshold of 90%.
Input: `.90`
that will create a threshold of .9%.
