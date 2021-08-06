import numpy as np
import cv2 as cv
import cv2
import re
import os

class Pictor:
    #circles = 0
    ellipses = 0
    triangles = 0
    polygons =0
    utilArea = 0
    R = 0
    G = 0
    B = 0
    LineWidth = 0
    number = 0


d = dict([])

fileDB = open("output.db", "r")
incr = 0
for linie in fileDB:
    if incr != 0:
        nume = ""
        p = Pictor()
        incr1 = 0
        for coloana in linie.strip().split():
            if incr1 == 0:
                nume = coloana
            #elif incr1 == 1:
             #   p.circles = coloana
            elif incr1 == 1:
                p.ellipses = int(coloana)
            elif incr1 == 2:
                p.triangles = int(coloana)
            elif incr1 == 3:
                p.polygons = int(coloana)
            elif incr1 == 4:
                p.utilArea = float(coloana)
            elif incr1 == 5:
                p.R = int(coloana)
            elif incr1 == 6:
                p.G = int(coloana)
            elif incr1 == 7:
                p.B = int(coloana)
            elif incr1 == 8:
                p.LineWidth = int(coloana)
            elif incr1 == 9:
                p.number = int(coloana)
            incr1 +=1
        d[nume] = p    
            
    incr += 1
    
fileDB.close()
 
listaFisiere = os.listdir("thrive")



for fisier in listaFisiere:
    img = cv2.imread("thrive/"+fisier)

    temp = re.compile("([a-zA-Z]+)([0-9]+)") 
    res = temp.match(fisier).groups()
    numePictor = res[0]

    
    rows,cols,chann = img.shape




    img = cv.medianBlur(img,5)


    imgray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

    thresh=cv2.Canny(imgray,30,200)

    contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

    img1=np.zeros((rows,cols,3), np.uint8)



    i = 0
  #  circles = 0
    triangles = 0
    polygons = 0
    sumAreas = 0
    mediumColor1 =0
    mediumColor2 =0
    mediumColor3 =0
    mediumwidth =0
    cnt1 = 0
    cnt2 = 0
    cnt3 = 0
    cnt4 = 0
    for cnt in contours:
        x1,y1,w1,h1 = cv2.boundingRect(cnt)
        if w1<=5 and h1>20:
            mediumwidth += w1
            cnt4 +=1
        polygons += 1
        approx = cv2.approxPolyDP(cnt, .03 * cv2.arcLength(cnt, True), True)
        area = cv2.contourArea(cnt)
        sumAreas += area

        M = cv2.moments(cnt)
        if M["m00"] !=0:
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
        if(cX<rows and cY<cols and cX !=0 and cY!=0):
            intensity = img[cX, cY];
            mediumColor1  += intensity[0]
            cnt1 += 1
            mediumColor2  += intensity[1]
            cnt2 += 1
            mediumColor3  += intensity[2]
            cnt3 += 1
        if len(approx)==3:
            if area > 5:
                triangles = triangles + 1
                cv2.drawContours(img1,[cnt],0,(0,0,255),1)
        elif len(approx)==4:
            area = cv2.contourArea(cnt)
            if area > 5:
                x,y,w,h = cv2.boundingRect(cnt)
                #if area == w*h:
                   # rectangles = rectangles + 1
                cv2.drawContours(img1,[cnt],0,(94,234,255),1)
        elif len(approx)==8:
            area = cv2.contourArea(cnt)
            (cx, cy), radius = cv2.minEnclosingCircle(cnt)
            circleArea = radius * radius * np.pi
            if circleArea == area:
                cv2.drawContours(img1, [cnt], 0, (220, 152, 91), 1)
            #    circles = circles + 1
        else:
            if len(approx)==1 or len(approx)==2 :
                   cv.drawContours(img1, [cnt], 0, (255,0,255), 1)  
            else:
                area = cv2.contourArea(cnt)
                (cx, cy), radius = cv2.minEnclosingCircle(cnt)
                circleArea = radius * radius * np.pi
                #if circleArea == area:
                   # circles = circles + 1
                i = i +1
                if i%3==0:
                    cv.drawContours(img1, [cnt], 0, (255,i,i), 1) 
                elif i%3==1:
                    cv.drawContours(img1, [cnt], 0, (0,255,i), 1)
                else:
                    cv.drawContours(img1, [cnt], 0, (0,i,255), 1) 


    ellipses =0
    detected_circles = cv2.HoughCircles(thresh,cv2.HOUGH_GRADIENT, 1, 50, param1 = 80, param2 = 20, minRadius = 3, maxRadius = 40)
    if detected_circles is not None: 
      
        # Convert the circle parameters a, b and r to integers. 
        detected_circles = np.uint16(np.around(detected_circles)) 
      
        for pt in detected_circles[0, :]:
            ellipses = ellipses +1
            a, b, r = pt[0], pt[1], pt[2] 
      
            # Draw the circumference of the circle. 
            cv2.circle(img1, (a, b), r, (255, 255, 255), 1)
            sumAreas += (3.14 * r *r)


            if(a<rows and b<cols and a !=0 and b!=0):
                intensity = img[a, b];
                mediumColor1  += intensity[0]
                cnt1 += 1
                mediumColor2  += intensity[1]
                cnt2 += 1
                mediumColor3  += intensity[2]
                cnt3 += 1

    print(numePictor)            
    #print ("circles:")
    #print (circles)
    print ("ellipses:")
    print (ellipses)
    print ("triangles:")
    print (triangles)
    print ("polygons:")
    print (polygons)
    print ("proportion of util area in total area:")
    print (sumAreas/(rows*cols))
    print ("medium color:")
    print (mediumColor1/cnt1)
    print (mediumColor2/cnt2)
    print (mediumColor3/cnt3)

    utilArea = sumAreas/(rows*cols)
    R = mediumColor1/cnt1
    G = mediumColor2/cnt2
    B = mediumColor3/cnt3
    if cnt4 != 0:
        mw = mediumwidth/cnt4
    
    if not(numePictor in d):
        p1 = Pictor()
        d[numePictor] = p1
    #d[numePictor].circles = int((d[numePictor].circles * d[numePictor].number + circles)/(d[numePictor].number+1))
    d[numePictor].ellipses = int((d[numePictor].ellipses * d[numePictor].number + ellipses)/(d[numePictor].number+1))
    d[numePictor].triangles = int((d[numePictor].triangles * d[numePictor].number + triangles)/(d[numePictor].number+1))
    d[numePictor].polygons = int((d[numePictor].polygons * d[numePictor].number + polygons)/(d[numePictor].number+1))
    d[numePictor].utilArea = (d[numePictor].utilArea * d[numePictor].number + utilArea)/(d[numePictor].number+1)
    d[numePictor].R =  int((d[numePictor].R * d[numePictor].number + R)/(d[numePictor].number+1))
    d[numePictor].G = int((d[numePictor].G * d[numePictor].number + G)/(d[numePictor].number+1))
    d[numePictor].B = int((d[numePictor].B * d[numePictor].number + B)/(d[numePictor].number+1))
    d[numePictor].LineWidth = int((d[numePictor].LineWidth * d[numePictor].number + mw)/(d[numePictor].number+1))
    d[numePictor].number += 1


fileDB = open("output.db", "w")
fileDB.write("Nume ellipses triangles polygons utilArea R G B LineWidth number")
fileDB.write("\n")

for a in d:
    fileDB.write( a + " " + str(d[a].ellipses) + " " + str(d[a].triangles) + " " + str(d[a].polygons) + " " + "{:.2f}".format(d[a].utilArea) + " " + str(d[a].R) + " " + str(d[a].G )+ " " + str(d[a].B) + " " + str(d[a].LineWidth) + " " + str(d[a].number))
    fileDB.write("\n")
fileDB.close()




