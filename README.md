## COMP3308 Introduction to Artificial Intelligence Assignments 

## Assignment 1: 
This task involves solving the 3-digit puzzle: Given two 3 digit numbers called 'start' and 'goal' and also a set of 3-digit numebrs called 'forbidden', we want to get from 'start' to 'goal' in the smallest number of moves. A move is defined as a transformation of one number into another number by adding ot subtracting 1 to one of its digits e.g. a move can take you from 123 to 124 by adding 1 to the last digit. 

Constraints: you cannot add the digit 9 or subtract from the digit 0, you cannot make a move that transforms the current number into one of the forbidden numbers, and you cannot change the same digit twice in two successive moves. 

The code in ThreeDigits.py solves the puzzle using 6 search strategies: breadth first search, depth first search, Greedy search, A* search, hill climbing and iterative deepening depth first search. 

## Assignment 2: 
This task involves implementing K-nearest neighbour and Naive Bayes algorithms to evaluate the Pima Indians Diabetes dataset. Code is stored in MyClassifier.py.
