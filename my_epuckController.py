from controller import Robot
import numpy as np
import cv2
robot = Robot()

timestep = int(robot.getBasicTimeStep())

left_motor = robot.getDevice('left wheel motor')
right_motor = robot.getDevice('right wheel motor')
left_motor.setPosition(float('inf'))
right_motor.setPosition(float('inf'))

left_motor.setVelocity(0.0)
right_motor.setVelocity(0.0)

camera = robot.getDevice('camera')
camera.enable(timestep)

def red_detect(frame):
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    lower_red1 = np.array([0, 100, 100])
    upper_red1 = np.array([10, 255, 255])

    lower_red2 = np.array([160, 100, 100])
    upper_red2 = np.array([180, 255, 255])

    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)

    mask = mask1 + mask2

    red_pixels = cv2.countNonZero(mask)
   
    if red_pixels > 500 :
        return True
    return False


def detect_colors(frame, min_pixels=500,):
   
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    detected = []
    # green
    lower_green = np.array([40, 70, 50])
    upper_green = np.array([90, 255, 255])
    green_mask = cv2.inRange(hsv, lower_green, upper_green)
    if cv2.countNonZero(green_mask) > min_pixels:
        # print("Green detected")
        return "green"
    
    

    # yellow (narrower; avoid catching brown/orange)
    lower_yellow = np.array([20, 120, 150])
    upper_yellow = np.array([35, 255, 255])
    yellow_mask = cv2.inRange(hsv, lower_yellow, upper_yellow)
    if cv2.countNonZero(yellow_mask) > min_pixels:
        # print("Yellow detected")
        return "yellow"
        # pink / magenta
    lower_pink = np.array([140, 50, 50])
    upper_pink = np.array([170, 255, 255])
    pink_mask = cv2.inRange(hsv, lower_pink, upper_pink)
    lower_pink2 = np.array([165, 30, 120])
    upper_pink2 = np.array([179, 255, 255])
    pink_mask = pink_mask | cv2.inRange(hsv, lower_pink2, upper_pink2)
    if cv2.countNonZero(pink_mask) > min_pixels:
        # print("Pink detected")
        return "pink"

        # brown (darker/desaturated orange) — tighter and with higher saturation cap for reliability
        # tuned to pick up colors like (R=165,G=105,B=30) while excluding bright yellow
    lower_brown = np.array([8, 100, 20])
    upper_brown = np.array([45, 255, 200])
    brown_mask = cv2.inRange(hsv, lower_brown, upper_brown)
    if cv2.countNonZero(brown_mask) > min_pixels:
        # print("Brown detected")
        return "brown"
    
        # resolve overlaps: prefer brown over yellow when both present
    if 'brown' in detected and 'yellow' in detected:
        detected.remove('yellow')

    return detected
# ...existing code...

ir_values = []
for i in range(8):
    ir = robot.getDevice(f'ps{i}')
    ir.enable(timestep)
    ir_values.append(ir)


state = False
printed_red = False
printed_yellow = False
printed_pink = False
printed_brown = False


while robot.step(timestep) != -1:

    ir_readings = [sensor.getValue() for sensor in ir_values]
    image = camera.getImage()
    widht = camera.getWidth()
    height = camera.getHeight()
    
   
    frame = np.frombuffer(image,np.uint8).reshape(height,widht,4)
    frame = frame[:,:,0:3]

    front_wall = ir_readings[0] > 80.0
    left_wall = ir_readings[1] > 80.0
    right_wall = ir_readings[7] > 80.0

    if red_detect(frame):
        if not printed_red: 
            print("Red detected - Starting color detection")
            printed_red = True
        state = True

    elif state:
         
        color= detect_colors(frame)
        if color == "yellow":
            if not printed_yellow:
                print("Yellow detected")
                printed_yellow = True
        elif color == "pink":
            if not printed_pink:
                print("Pink detected")
                printed_pink = True
        elif color == "brown":
            if not printed_brown:
                print("Brown detected")
                printed_brown = True
        
        
        if color == "green":
            print("Green Detected - Stopping at green")
            left_motor.setVelocity(0.0)
            right_motor.setVelocity(0.0)
            break

    if front_wall:
        left_motor.setVelocity(-1.0)
        right_motor.setVelocity(6.28)
    
    else:
        if left_wall:
          
            left_motor.setVelocity(6.28)
            right_motor.setVelocity(6.28)
        else:
           
            left_motor.setVelocity(5.0)
            right_motor.setVelocity(1.0)

        if right_wall:
            left_motor.setVelocity(5.0)
            right_motor.setVelocity(1.0)
      