#domino a,b play, 6X6
import random


def dfree(i, j):
  df = []
  if i < 5 and l[i + 1][j] == 0:
    df.append((i + 1, j))
  if j < 5 and l[i][j + 1] == 0:
    df.append((i, j + 1))
  if i > 0 and l[i - 1][j] == 0:
    df.append((i - 1, j))
  if j > 0 and l[i][j - 1] == 0:
    df.append((i, j - 1))
  return df

def ringmin(ring):
  min=3
  for ij in ring:
    i, j = ij[0], ij[1]
    if l[i][j] == 0:
      ldf = len(dfree(i, j))
      if min > ldf:
        min = ldf
  return min


path = [[(0, 0), (0, 1), (0, 2), (0, 3), (0, 4), (0, 5), (1, 5), (2, 5), (3, 5), (4, 5), (5, 5), (5, 4), (5, 3), (5, 2),
         (5, 1), (5, 0), (4, 0), (3, 0), (2, 0), (1, 0)], \
        [(1, 1), (1, 2), (1, 3), (1, 4), (1, 4), (2, 4), (3, 4), (4, 4), (4, 3), (4, 2), (4, 1), (3, 1), (2, 1)], \
        [(2, 2), (3, 2), (3, 3), (2, 3)]]
#path contains the 3 rings coordinates in order,as 3 lists of tuples.
lost = False
for m in range(1000000):
  t = 0
  if lost == False:
    l = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]

    for ring in path:#ind in range(1):
      rl=len(ring)
      for x in range(12):
        rlflag=False

        for ij in ring:
          #ij=path[ind]
          i,j = ij[0],ij[1]
          if l[i][j]==0:
            rlflag = True
            df = dfree(i, j)
            l1 = len(df)
            if l1==ringmin(ring):
              t += 1
              l[i][j] = t
              if l1>0:
                play = random.randint(0,l1-1)
                pi=df[play][0]
                pj=df[play][1]

                l[pi][pj]=t
              else:
                lost=True
                print('\nA lost')
                for i in range(6):
                  print(l[i])
                break
        if rlflag == False:
          #print('ring complete', ring)
          #for i in range(6):
          #  print(l[i])
          break
print()
for i in range(6):
  print(l[i])