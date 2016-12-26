import math

def sigmoid(z):
    return 1.0/(1.0 + math.e**(-z))

print "S(0)= ", sigmoid(0)
print "S(10)= ", sigmoid(10)
print "S(-10)= ", sigmoid(-10)