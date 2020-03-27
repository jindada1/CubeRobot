import cv2
import matplotlib.pyplot as plt

bgr = cv2.imread('in/Cube_0.png')
b,g,r = cv2.split(bgr)
hsv = cv2.cvtColor(bgr, cv2.COLOR_BGR2HSV)
h,s,v = cv2.split(hsv)

fig=plt.figure(figsize=(8, 4))

imgs = [bgr, b, g, r, hsv, h, s, v]
titles = ['bgr', 'b', 'g', 'r', 'hsv', 'h', 's', 'v']

columns = 4
rows = 2
for i in range(1, columns*rows +1):
    fig.add_subplot(rows, columns, i)
    plt.imshow(imgs[i - 1])
    plt.title(titles[i - 1])
    plt.axis('off')

plt.show()
