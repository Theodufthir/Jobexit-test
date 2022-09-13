# Jobexit-test
A small test project for a stage in Jobexit, written in Python

# What is it
It is a simulator the computes the percentage of salary compared to full time per month.
To compute this, the program takes a list of periods of part time with the rate of work compared to full time associated, and the dates of the beginning and end of the employement.

# Requirements
- Python 3.10

# Installation
You only need to clone the repository

# Usage
This program can be launched using python 3.10 as follows : `python main.py arg1 arg2 arg3`
arg1 to arg3 represent the 3 string arguments needed by the program, they are respectively the list of periods of part time, the start date of the employement and the end date of the employement.

All dates follow the format "YYYY-MM-DD" and the rates are to be inputed as decimals (for example 0.5 for 50%).
The list is comprised of tuples using the format "(date,date,rate)", and the list itself is using the format "[tuple,tuple]" with any number of tuples separated by commas.

So for a job that starts the 1st of january 2019, ends the 31st of december 2019 and has a part time period at a rate of 80% starting on the 16th of june, the command would be :
`python main.py '[(2019-06-16,2019-12-31,0.8)]' 2019-01-01 2018-12-31`

