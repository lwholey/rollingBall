def createPathPoints():
	xPts = [1, 3, 5, 7, 9]
	yPts = [10, 30, 50, 70, 90]
	return xPts, yPts

def findFirstGreater(xPts, yPts, target):
  cnt = 0
  for x in xPts:
    if x > target:
      y = yPts[cnt]
      return x, y
    cnt = cnt + 1
  return None

targetValue = 7
xPts, yPts = createPathPoints()
xt, yt = findFirstGreater(xPts, yPts, targetValue)

if xt:
  print("The first value greater than", targetValue, "is:", xt)
  print("The corresponding y value is:", yt)
else:
  print("No value greater than", targetValue, "found in the list.")
