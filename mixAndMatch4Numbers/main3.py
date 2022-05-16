#montey hall 2 cars, 4 cells
import random
won=0
lost=0
r=200000


def switch():
  for i in range(len(c)):
    if l[i]==0 and c[i]==0:
      l.pop(i)
      c.pop(i) # choice list
      for i in range(len(c)): #move
        if c[i]==1:
          c[i-1],c[i]=c[i],c[i-1]
          break
      break

for x in range(r):
  l = [0, 0, 0, 0]
  c = [0, 0, 0, 0]
  c[random.randint(0,3)]=1
  l[random.randint(0,3)]=1 #location of the car
  #n=random.randint(0,3) # insert another car.
  #if l[n]==0:
  #  l[n]=1
  #else:
  #  l[n-1]=1

  switch()
  for i in range(len(c)):
    if c[i]==1:
      if l[i]==1:
        won+=1
      else:
        lost+=1
      break;



print (won/r)