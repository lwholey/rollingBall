import math

def createPathPoints():
	xPts = [1, 3, 5, 7, 9]
	yPts = [100, 70, 55, 45, 42]
	return xPts, yPts

def findFirstGreater(xPts, yPts, target):
  cnt = 0
  for x in xPts:
    if x > target:
      y = yPts[cnt]
      return x, y
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


px = 10
py = 100
vx = 1
vy = 0
t = 0
dt = 0.01
theta = 90 * math.pi / 180
print("theta is", theta)

#targetValue = 7
xPts, yPts = createPathPoints()
#xt, yt = findFirstGreater(xPts, yPts, targetValue)

while t < 2:
  px, py, vx, vy, t = integratePosVel(px, py, vx, vy, t, dt, theta)
  print("px", px, 'py', py, "vx", vx, 'vy', vy)

