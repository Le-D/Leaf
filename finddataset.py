import cv2
import imutils
import numpy as np
import xlsxwriter





def findLeaf(leafImage):
    
    #leafImage = leafImage + str(l) + ".jpg"
    
    imOriginal = cv2.imread(leafImage)
    imContourLeaf = imOriginal.copy()
    imContourLeafY = imOriginal.copy()
    imContourLeafX = imOriginal.copy()
    imHullConvex = imOriginal.copy()


    
    dataStr = ""

####Pre-processiong start
    
    imContourLeaf = cv2.cvtColor(imContourLeaf,cv2.COLOR_BGR2GRAY)
    #cv2.imwrite("imContourLeafGray.jpg",imContourLeaf)
    
    imContourLeaf = cv2.GaussianBlur(imContourLeaf, (7, 7), 0)
    #cv2.imwrite("imContourLeafBlur.jpg",imContourLeaf)
    
    ret,imContourLeaf = cv2.threshold(imContourLeaf,160,255,0)
    #cv2.imwrite("imContourLeafThresh.jpg",imContourLeaf)

    imContourLeaf = cv2.erode(imContourLeaf, None, iterations=7)
    #cv2.imwrite("imContourLeafErode.jpg",imContourLeaf)
    imContourLeaf = cv2.dilate(imContourLeaf, None, iterations=7)
    #cv2.imwrite("imContourLeafDilate.jpg",imContourLeaf)

    imContourLeaf = cv2.bitwise_not(imContourLeaf)
    #cv2.imwrite("bitwise_not.jpg",imContourLeaf)

    imLeafY = imContourLeaf.copy()
    imLeafX = imContourLeaf.copy()
    
    imContourHullConvex = imContourLeaf.copy()

    
####Pre-processiong end

####Find leaf contour start
    
    _, contoursLeaf,_ = cv2.findContours(imContourLeaf,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)

    cv2.drawContours(imOriginal,contoursLeaf,-1,(255,0,0),2)
    #cv2.imshow('bb',imOriginal)
    #cv2.imwrite("contoursLeaf.jpg",imOriginal)
    
    cnt = contoursLeaf[-1]
    x,y,w,h = cv2.boundingRect(cnt)
    #cv2.rectangle(imOriginal,(x,y),(x+w,y+h),(255,255,255),1)
    #cv2.rectangle(imContourLeafY,(x,y),(x+w,y+h),(255,255,255),1)
    #cv2.rectangle(imContourLeafX,(x,y),(x+w,y+h),(255,255,255),1)
    
    area = cv2.contourArea(cnt)
    perimeter = cv2.arcLength(cnt,True)
    
    perimeter = round(perimeter,6)

    ratioPeri_Area = perimeter/area
    
    ratioPeri_Area = round(ratioPeri_Area,6)
    

    dataStr += str(area)+"\t"
    dataStr += str(perimeter)+"\t"
    dataStr += str(ratioPeri_Area)+"\t"
    
    print ("Leaf area :", area)
    print ("Leaf perimeter :", perimeter)
    print ("Ratio Perimeter/Area :", ratioPeri_Area)

    #cv2.imwrite("leafboundingRect.jpg",imOriginal)
    
    
####Find leaf contour end
    
####Segment on y-axis start

    pxstepY = int(w/15)
    pxstepX = int(h/15)

    box_width = x+w
    box_height = y+h

    xseg = x
    
    while x < box_width:
        cv2.line(imLeafY, (x, y), (x, box_height), color=(0, 0, 0), thickness=1)
        #cv2.line(imContourLeafY, (x, y), (x, box_height), color=(255, 255, 255), thickness=1)
        x += pxstepY

    #cv2.imwrite("leafSegY.jpg",imContourLeafY)

    _, contoursLineY, hierarchy = cv2.findContours(imLeafY,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    #cv2.drawContours(imContourLeafY,contoursLine,-1,(255,255,255),1)
    #cv2.imshow('vasdva',imContourLeafY)
    
    valY = []
    for i, c in enumerate(contoursLineY):
        area = cv2.contourArea(c)
        cnt = contoursLineY[i]
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(imContourLeafY,(x,y),(x+w,y+h),(255,255,255),1)
        
        valY.append(h)
        
        #dataStr += str(h)+"\t"
        
    #print ("Y-segment list : ", valY)

    largest_area = 0
    second_area = 0
    l_index = 0
    s_index = 0
    for i, c in enumerate(contoursLineY):
        area = cv2.contourArea(c)
        if (area > largest_area):
            if (area > second_area):
                second_area = largest_area
                largest_area = area
                l_index = i
        elif (area > second_area):
            second_area = area
            s_index = i


    cnt = contoursLineY[l_index]
    x,y,w,h = cv2.boundingRect(cnt)
    #cv2.rectangle(imContourLeafY,(x,y),(x+w,y+h),(0,0,255),2)
    
    #cv2.imshow('originalY',imContourLeafY)
    #cv2.imshow('y-axis',imLeafY)
    
    #cv2.imwrite("imContourLeafY.jpg",imContourLeafY)
    #cv2.imwrite("imLeafY.jpg",imLeafY)

####Segment on y-axis end

####Segment on x-axis start

    while y < box_height:
        cv2.line(imLeafX, (xseg, y), (box_width, y), color=(0, 0, 0), thickness=1)
        #cv2.line(imContourLeafX, (xseg, y), (box_width, y), color=(255, 255, 255), thickness=1)

        y += pxstepX

    #cv2.imwrite("leafSegX.jpg",imContourLeafX)

    _, contoursLineX, hierarchy = cv2.findContours(imLeafX,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    valX = []

    for i, c in enumerate(contoursLineX):
        area = cv2.contourArea(c)
        cnt = contoursLineX[i]
        x,y,w,h = cv2.boundingRect(cnt)
        cv2.rectangle(imContourLeafX,(x,y),(x+w,y+h),(255,255,255),1)
        
        valX.append(w)
        
        #dataStr += str(w)+"\t"

        
    #print ("X-segment list : ", valX)
    
    
    largest_area = 0
    second_area = 0
    l_index = 0
    s_index = 0
    for i, c in enumerate(contoursLineX):
        area = cv2.contourArea(c)
        if (area > largest_area):
            if (area > second_area):
                second_area = largest_area
                largest_area = area
                l_index = i
        elif (area > second_area):
            second_area = area
            s_index = i

    cnt = contoursLineX[l_index]
    x,y,w,h = cv2.boundingRect(cnt)
    #cv2.rectangle(imContourLeafX,(x,y),(x+w,y+h),(0,0,255),2)
    
    #.imshow('originalX',imContourLeafX)
    #cv2.imshow('x-axis',imLeafX)
    
    #cv2.imwrite("imContourLeafX.jpg",imContourLeafX)
    #cv2.imwrite("imLeafX.jpg",imLeafX)
    
####Segment on x-axis end
    
####Segment on Hullconvex start
    
    #imContourHullConvex
    
    #img_gray = cv2.cvtColor(imContourHullConvex,cv2.COLOR_BGR2GRAY)
    
    #ret,img_gray = cv2.threshold(img_gray,160,255,0)
    

    cv2.imshow('Ori',imContourHullConvex)

    _,contours,hierarchy = cv2.findContours(imContourHullConvex,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    
    countDefects = 0

    for cnt in contours:
        hull = cv2.convexHull(cnt)
        #cv2.drawContours(imHullConvex,[cnt],0,(0,255,0),2)   # draw contours in green color
        cv2.drawContours(imHullConvex,[hull],0,(0,255,255),2)  # draw contours in red color
        
        areaHull = cv2.contourArea(hull)
        #print("Hull area: ",areaHull)

        perimeterHull = cv2.arcLength(hull,True)
        #print("Hull perimeter: ",perimeterHull)
        
        ratioHull_Peri_Area = perimeterHull/areaHull
        #print("Ratio Hull: ",ratioHull_Peri_Area)

        
        cnt = cv2.approxPolyDP(cnt,0.01*cv2.arcLength(cnt,True),True)
        hull = cv2.convexHull(cnt,returnPoints = False)
        
        defects = cv2.convexityDefects(cnt,hull)
        

        if defects is not None:

            for i in range(defects.shape[0]):
                            
                s,e,f,d = defects[i,0]
                start = tuple(cnt[s][0])
                end = tuple(cnt[e][0])
                far = tuple(cnt[f][0])
                cv2.line(imHullConvex,start,end,[0,255,0],2)
                cv2.circle(imHullConvex,far,5,[0,0,255],-1)
                
                countDefects +=1
                
        else:
            defects = 0

    perimeterHull = round(perimeterHull,6)
    ratioHull_Peri_Area = round(ratioHull_Peri_Area,6)
              
    print ("Convexity: ",countDefects)
    
    print("Hull area: ",areaHull)
    print("Hull perimeter: ",perimeterHull)
    print("Ratio Hull: ",ratioHull_Peri_Area)
    
    

    
    dataStr += str(countDefects)+"\t"
    
    dataStr += str(areaHull)+"\t"
    dataStr += str(perimeterHull)+"\t"
    dataStr += str(ratioHull_Peri_Area)+"\t"

    cv2.imshow('HullConvex',imHullConvex)

        
    
    
	

    
####Segment on Hullconvex end
 
    #return l_index
    
    dataStr += "\n"

    text_file = open("leaf_data.txt", "a")
    #text_file.write("{}\t{}\t".format(area, perimeter))
    text_file.write("{}".format(dataStr))
    
    text_file.close()
    

#leafImage = "lime1.jpg"

leafNum = 1
    
while leafNum < 50:
        
    l = leafNum
    
    print(l)
    
    leafImage = "Mandarin/mandarin"
    #leafImage = "Chili/chili"
    #leafImage = "Eggplant/eggplant"

    leafImage += str(l)
    leafImage += ".jpg"
    
    findLeaf(leafImage)
    
    leafNum += 1



cv2.waitKey(0)
cv2.destroyAllWindows()