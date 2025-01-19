import math

def createPathPoints():
	xPts = [1, 3, 5, 7, 9]
	yPts = [100, 70, 55, 45, 42]
	return xPts, yPts


def findTheta(x, xPts, yPts):
  x2, y2, cnt = findFirstGreater(xPts, yPts, x)
  if cnt - 1 < 0:
  	raise Exception("Sorry, no numbers below zero")
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


px = 3.01
py = 100
vx = 0
vy = 0
t = 0
dt = 0.01

xPts, yPts = createPathPoints()

while t < 2:
  theta = findTheta(px, xPts, yPts)
  px, py, vx, vy, t = integratePosVel(px, py, vx, vy, t, dt, theta)
  print("px %0.2f" % px, 'py %0.2f' % py, "vx %0.2f" % vx, 'vy %0.2f' % vy)
  print("theta is %0.2f" % (theta*180/math.pi), "deg")

