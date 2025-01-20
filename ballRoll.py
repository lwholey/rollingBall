import math

# TODO:
# Create path points using the Brachistrochone problem
# test straight path drops for reasonableness
# through an error if total massless energy changes by a certain amount
# check if ball drops below path
# add drag/friction options
# add ball rotation dynamics
def createPathPoints(py, rCyc):
	# py is starting y point on curve
	# rCyc is cycloid radius
	r = rCyc
	xPts = []
	yPts = []
	t = 0
	dt = 0.001
	while t < (2 * math.pi):
		x = r * (t - math.sin(t))
		y = -r * (1 - math.cos(t)) + py
		xPts.append(x)
		yPts.append(y)
		t = t + dt
	#xPts = [1, 3, 5, 7, 9, 11, 13, 15, 17]
	#yPts = [100, 70, 55, 45, 42, 60, 80, 100, 200]
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

def getTotalEnergy(py, vx, vy):
  # find the massless total energy
  speed = getSpeed(vx, vy)
  ke = 0.5 * speed * speed
  pe = getG() * py
  te = pe + ke
  #print("Total massless energy %0.2f" % te)
  return te

def checkTotalEnergy(px, vx, vy, te0):
  te = getTotalEnergy(py, vx, vy)
  if math.fabs(te - te0) > 0.001:
    raise Exception("Previous Total massless energy %0.2f" % te0, "Changed to %0.2f" % te, "Too large?")
  return te

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

rCyc = 58.5 # cycloid radius (m) 
px = 0
py = 100
vx = 0
vy = 0
t = 0
dt = 0.01

xPts, yPts = createPathPoints(py, rCyc)
theta0 = findTheta(px, xPts, yPts)
te0 = getTotalEnergy(py, vx, vy) # initial total massless energy

while t < 8:
  theta = findTheta(px, xPts, yPts)
  if theta0 != theta: # new slope
    vx, vy = correctVelToFitPath(vx, vy, theta)
    te0 = checkTotalEnergy(px, vx, vy, te0)
  px, py, vx, vy, t = integratePosVel(px, py, vx, vy, t, dt, theta)
  print("px %0.2f" % px, 'py %0.2f' % py, "vx %0.2f" % vx, 'vy %0.2f' % vy)
  theta0 = theta
