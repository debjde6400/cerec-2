import random

highest = 10
answer = random.randrange(highest)
guess = input("Guess a number from 0 to %d : " %highest)
while(int(guess)!=answer):
     if(int(guess) < answer):
          print("Answer is higher")
     else:
          print("Answer is lower")
     guess = input("Guess a number from 0 to %d : " %highest)
input("You are a winner face!")
