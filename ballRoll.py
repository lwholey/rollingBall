import math

def createPathPoints():
	xPts = [1, 3, 5, 7, 9, 11, 13, 15, 17]
	yPts = [100, 70, 55, 45, 42, 60, 80, 100, 110]
	return xPts, yPts

def correctVelToFitPath(vx, vy, theta):
  speed = math.sqrt(vx*vx + vy*vy)
  vx = speed * math.sin(theta)
  vy = speed * math.cos(theta)
  return vx, vy

def findTheta(x, xPts, yPts):
  if x == xPts[0]:
    x = x + 0.00001 # offset by a small amount to avoid error at the boundary
  x2, y2, cnt = findFirstGreater(xPts, yPts, x)
  if cnt - 1 < 0:
  	raise Exception("Sorry, no numbers below zero. X position of %0.2f" % x, "is probably too small")
  x1 = xPts[cnt-1]
  y1 = yPts[cnt-1]
  m = (y2-y1)/(x2-x1)
  theta = math.atan(m)
  if theta < 0:
    theta = theta + math.pi
  return theta

def findFirstGreater(xPts, yPts, target):
  cnt = 0
  for x in xPts:
    if x >= target:
      y = yPts[cnt]
      return x, y, cnt
    cnt = cnt + 1
  raise Exception("Sorry, no numbers found. X position of %0.2f" % target, "is probably too large")
  return None

def integratePosVel(px0, py0, vx0, vy0, t0, dt, theta):

  g = 9.81 # gravity in meters/second^2
  
  ax = -g * math.cos(theta) * math.sin(theta)
  ay = -g * math.sin(theta) * math.sin(theta)

  vxf = vx0 + ax * dt
  vyf = vy0 + ay * dt

  pxf = px0 + vx0 * dt + 0.5 * ax * dt*dt
  pyf = py0 + vy0 * dt + 0.5 * ay * dt*dt


  tf = t0 + dt

  return pxf, pyf, vxf, vyf, tf


px = 1
py = 100
vx = 0
vy = 0
t = 0
dt = 0.01

xPts, yPts = createPathPoints()

while t < 5:
  theta = findTheta(px, xPts, yPts)
  vx, vy = correctVelToFitPath(vx, vy, theta)
  px, py, vx, vy, t = integratePosVel(px, py, vx, vy, t, dt, theta)
  print("px %0.2f" % px, 'py %0.2f' % py, "vx %0.2f" % vx, 'vy %0.2f' % vy)
  print("theta is %0.2f" % (theta*180/math.pi), "deg")

