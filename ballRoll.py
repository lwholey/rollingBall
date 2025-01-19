import math

# TODO:
# Create path points using the Brachistrochone problem
# add drag/friction options
# add ball rotation dynamics
def createPathPoints():
	xPts = [1, 3, 5, 7, 9, 11, 13, 15, 17]
	yPts = [100, 70, 55, 45, 42, 60, 80, 100, 200]
	return xPts, yPts

def correctVelToFitPath(vx, vy, theta):
  # theta is different for velocity and should range between -pi/2 and pi/2
  vx0 = vx
  if theta > math.pi / 2:
    theta = theta - math.pi
  print("1 vx %0.2f" % vx, 'vy %0.2f' % vy, "theta (deg) %0.2f" % (theta*180/math.pi))
  speed = getSpeed(vx, vy)
  vx = speed * math.cos(theta)
  vy = speed * math.sin(theta)
  # handle the case where ball was travelling backwards (in negative x direction)
  if vx0 < 0:
    vx = -vx
    vy = -vy
  print("2 vx %0.2f" % vx, 'vy %0.2f' % vy, "theta (deg) %0.2f" % (theta*180/math.pi))
  return vx, vy

def getSpeed(vx, vy):
  speed = math.sqrt(vx*vx + vy*vy)
  return speed

def findTheta(x, xPts, yPts):
  # theta for acceleration  should range between 0 and pi
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

def  checkTotalEnergy(py, vx, vy):
  # find the massless total energy
  speed = getSpeed(vx, vy)
  ke = 0.5 * speed * speed
  pe = getG() * py
  te = pe + ke
  print("Total massless energy %0.2f" % te)

def getG():
	return 9.81 # gravity in meters/second^2

def integratePosVel(px0, py0, vx0, vy0, t0, dt, theta):

  g = getG()
  
  ax = -g * math.cos(theta) * math.sin(theta)
  ay = -g * math.sin(theta) * math.sin(theta)
  #print("ax %0.2f" % ax, "ay %0.2f" % ay)
  #print("acceleration magnitude %0.2f" % getSpeed(ax, ay))

  vxf = vx0 + ax * dt
  vyf = vy0 + ay * dt

  #print("dt %0.2f" % dt)
  #print("vxf %0.2f" % vxf, "vyf %0.2f" % vyf)

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
theta0 = findTheta(px, xPts, yPts)


while t < 8:
  theta = findTheta(px, xPts, yPts)
  if theta0 != theta: # new slope
    vx, vy = correctVelToFitPath(vx, vy, theta)
    checkTotalEnergy(py, vx, vy)
  px, py, vx, vy, t = integratePosVel(px, py, vx, vy, t, dt, theta)
  print("px %0.2f" % px, 'py %0.2f' % py, "vx %0.2f" % vx, 'vy %0.2f' % vy)
  theta0 = theta
