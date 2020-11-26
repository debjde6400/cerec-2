# -*- coding: utf-8 -*-
"""
Created on Wed Nov 18 21:39:44 2020

@author: Shaunak
"""


# Name: *** Enter your name here ***
#
# Student-ID: *** Enter your student ID here ***
#
# Rename the file to <yourname>03.py
#


# Exercise 1A
#
# Implement a "Hello, World!" program
#
def hello_world():
    """
    Saying 'Hello, World!'
    """
    # *** Remove the keyword 'pass' and insert your program
    # code here ***
    print ('Hello, World!')


# Exercise 1B
#
# Implement a function that prints the beer song to
# standard output. The song starts with "99 bottles of
# beer, etc."
#
def beersong(n_beer=99):
    """
    Singing "99 bottles of beer" 'til the very end
    """
    # *** Remove the keyword 'pass' and insert your program
    # code here ***
    while n_beer>1:
        print(n_beer, 'bottles of beer on the wall,') 
        print(n_beer, 'bottles of beer Take one down, pass it around,')
        n_beer = n_beer-1
    if n_beer==1:
       print('1 bottle of beer on the wall, 1 bottle of beer Take it down, pass it around,')
       n_beer = n_beer-1
    if n_beer == 0:
       print ('No more bottles of beer on the wall, no more bottles of beer Go to the store and buy some more.')
    
# Exercise 2
#
# In this exercise, we calculate the sum of the numbers
# from some initial number "start" until a final number "end"
# in various ways.
#
# Exercise 2A
#
# Sum of the series is calculated by using the built-in
# function sum and range
#
def addup(start, end):
    """
    Summing the numbers from 'start' to 'end' using the 
    built-in functions sum and range                                    
    """
    # *** Remove the keyword 'pass' and insert your program
    # code here ***
    a=range(start, end+1)
    sum(a)
    print(sum(a))
    return 


# Exercise 2B
#
# Sum of the series with a for loop
#
def addup2(start, end):
    """
    Summing the numbers from 'start' to 'end' using a for
    loop
    """
    # *** Remove the keyword 'pass' and insert your program
    # code here ***
    sum=0
    for i in range(start, end+1):
        sum=sum+i
    return sum
    


# Exercise 2C
#
# Sum of the series with a while loop
#
def addup3(start, end):
    """
    Summing the numbers from 'start' to 'end' using a while
    loop
    """
    # *** Remove the keyword 'pass' and insert your program
    # code here ***
    sum=0
    a=start
    while a<=end:
        sum=sum+a
        a=a+1
    return sum
    


# Exercise 2D
#
# Sum of the series using Gauss' method
#                                                          
def addup4(start, end):
    """
    Summing the numbers from 'start' to 'end' using young
    Carl-Friedrich's trick
    """
    # *** Remove the keyword 'pass' and insert your program
    # code here ***
    sum=(start + end)*(((end-start)/2)+0.5)
    return sum


# Exercise 3A
#
# Implement a function for converting a nonnegative decimal
# number to an (unsigned) binary number represented as a
# string of 0's and 1's using successive halving
#                                                          
def halving(decimal):
    """
    Converts decimal input number to binary using successive
    halving
    """
    # *** Remove the keyword 'pass' and insert your program
    # code here ***
    if decimal<0:
        return
    bitstring=''
    q=decimal
    while q!=1:
        r=q%2
        bitstring = str(r)+bitstring
        q=q//2
    bitstring = str(q)+bitstring
    return bitstring


# Exercise 3B
#
# Implement a function for converting an (unsigned) binary
# number represented as a string of 0's and 1's (a bit string)
# to a decimal number using successive doubling
#
def doubling(binary):
    """
    Converts a bit string to a decimal number using successive
    doubling
    """
    # *** Remove the keyword 'pass' and insert your program
    # code here ***
    number=0
    rev_s=''
    for c in binary:
        rev_s=c+rev_s
    
    i=0
    for d in rev_s:
        if(d == '1'):
            number+=2**i
        i+=1
    return number
        


# Test code - you shouldn't change this part of the code unless you
# know what you are doing

if __name__ == '__main__':
    #
    # This part of the script tests your code by successively calling
    # all function. If you want to skip the execution of a function
    # simply put a comment sign "#" in front of the line executing the
    # code.
    #
    # Please remember that correct indentation is essential in Python,
    # i.e. every statement in this section should be indented.
    #
    start, end = 1, 100
    decimal = 1234
    binary = '10011010010'
    
    exercises = {'1A': (hello_world, ), 
                 '1B': (beersong, 99),
                 '2A': (addup, start, end),
                 '2B': (addup2, start, end),
                 '2C': (addup3, start, end),
                 '2D': (addup4, start, end),
                 '3A': (halving, decimal),
                 '3B': (doubling, binary)}

    choice = input('Please enter the number of the exercise: ').upper()
    if choice not in exercises:
        print('Please choose among {0}'.format(
            list(exercises.keys())))
    else:
        func, *args = exercises[choice]
        print('Task {0}, testing function "{1}"'.format(
            choice, func.__name__))
        result = func(*args)
        if result is not None:
            print('Result:', result)
            