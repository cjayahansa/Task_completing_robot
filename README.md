
## **Webots Color Detect Wall-Following Robot**

This project is a simple Webots controller program.
The robot follows walls using IR sensors and uses the camera to detect colors.

### **Features**

* Wall following using 8 IR sensors
* Detect **red** → start checking other colors
* Detect **yellow, pink, brown** → print only once
* Detect **green** → stop the robot
* Uses HSV color filtering with OpenCV

### **Flow**

1. Robot moves and follows walls
2. Sees red → activate color detection mode
3. Detects colors one by one
4. Sees green → robot stops

### **Technologies**

* Python
* OpenCV
* Webots robot simulator

---
