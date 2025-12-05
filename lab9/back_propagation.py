import math
print(0.1*0.662*(-0.0406)+0.8731)
print(0.1*0.6797*(-0.0406)+0.0991)
print(0.1*0.662*(-0.0406)+0.7976)
print(0.1*0.6797*(-0.0406)+0.3971)
print(0.1*0.662*(-0.0406)+0.5926)
def sigmoid(x):
    return 1 / (1 + math.exp(-x))

# Initial parameters
x1 = 0.35
x2 = 0.9
w11 = 0.0991
w12 = 0.3971
w21 = 0.7976
w22 = 0.5926
w13 = 0.2724
w23 = 0.8731
mu = 0.1
y_f = 0.5

# Print header
print("Iteration | w11    | w12    | w21    | w22    | w13    | w23    | H1     | H2     | y3     ")

# For iteration 0: initial weights, no computations
print(f"0         | {w11:.4f} | {w12:.4f} | {w21:.4f} | {w22:.4f} | {w13:.4f} | {w23:.4f} |        |        |        ")

for i in range(1, 6):
    # Forward pass
    H1 = x1 * w11 + x2 * w21
    y1 = sigmoid(H1)
    H2 = x1 * w12 + x2 * w22
    y2 = sigmoid(H2)
    H3 = y1 * w13 + y2 * w23
    y3 = sigmoid(H3)
    
    # Print current state
    print(f"{i}         | {w11:.4f} | {w12:.4f} | {w21:.4f} | {w22:.4f} | {w13:.4f} | {w23:.4f} | {H1:.4f} | {H2:.4f} | {y3:.4f}")
    
    # Backward pass
    delta3 = y3 * (1 - y3) * (y_f - y3)
    delta1 = y1 * (1 - y1) * (w13 * delta3)
    delta2 = y2 * (1 - y2) * (w23 * delta3)
    
    # Update weights
    w11 = w11 + mu * x1 * delta1
    w21 = w21 + mu * x2 * delta1
    w12 = w12 + mu * x1 * delta2
    w22 = w22 + mu * x2 * delta2
    w13 = w13 + mu * y1 * delta3
    w23 = w23 + mu * y2 * delta3