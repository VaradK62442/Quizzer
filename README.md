## General quiz application
Reads in JSON file of question-answer pairs.
Randomly asks user the questions, and shows table of results with some basic (temperamental) answer checking.

You can specify command line arguments when running the program to specify which portion of questions to use, i.e. ```python main.py 0 50``` will select half of the questions in the file you specify, ```python main.py 0 25``` will select one quarter, etc.

You may need to download the ```scikit``` module, which can be done by running ```pip install scikit-learn```