# Define the modulus for the elliptic curve operations
MODULUS = 17

# Define the addition formula for points on the elliptic curve
def elliptic_add(P, Q):
    if P == (0, 0):
        return Q
    if Q == (0, 0):
        return P
    if P[0] == Q[0] and (P[1] != Q[1] or P[1] == 0):
        # P + Q = O (the "point at infinity") if P and Q are inverse to each other or if we're trying to add a point 
        # to itself but its y-coordinate is 0 (the result of point doubling a point on the x-axis)
        return (0, 0)
    if P == Q:
        # Point doubling case
        lam = (3 * P[0]**2) * pow(2 * P[1], -1, MODULUS)
    else:
        # Point addition, P != Q
        lam = (Q[1] - P[1]) * pow(Q[0] - P[0], -1, MODULUS)
    lam %= MODULUS
    x3 = (lam**2 - P[0] - Q[0]) % MODULUS
    y3 = (lam * (P[0] - x3) - P[1]) % MODULUS
    return (x3, y3)

# Define the initial point P
P = (3, 1)

# Scalar k in binary (excluding the leading 1)
k_binary = '01' # The binary representation of 5 is 101, excluding the leading 1

# Initialize the current point as P
current_point = P

# Execute the double and add algorithm according to the steps provided
for bit in k_binary:
    # Always double the current point
    current_point = elliptic_add(current_point, current_point)
    
    # If the current bit is 1, add P to the current point
    if bit == '1':
        current_point = elliptic_add(current_point, P)

# The final current_point would be kP, which is 5P in this case
print(current_point)
