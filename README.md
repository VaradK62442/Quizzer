## General quiz application
Reads in JSON file of question-answer pairs.
Randomly asks user the questions, and shows table of results with some basic (temperamental) answer checking.

You can specify command line arguments when running the program to specify which portion of questions to use, i.e. ```python main.py 0 50``` will select half of the questions in the file you specify, ```python main.py 0 25``` will select one quarter, etc.

Requirements needed are listed in the requirements file, and can be downloaded using
```pip install -r requirements.txt```
