import cv2 as cv
import numpy as np

class Mapping:
    def __init__(self,main_img,temp_img): #ประกาศClassที่เริ่มต้น รับค่าของรูปหลัก และ รูปย่อย
        # read img
        #self.mainimg = cv.imread(main_img,cv.IMREAD_ANYCOLOR) #เอารูปไปแปลงเป็นตัวเลข numpy arry
        self.mainimg = main_img
        self.tempimg = cv.imread(temp_img,cv.IMREAD_ANYCOLOR) #เอารูปไปแปลงเป็นตัวเลข numpy arry
        # end read
        
    def search(self,threshold:float=0.88,txt="",debug=False):
        result = cv.matchTemplate(self.mainimg,self.tempimg,cv.TM_CCOEFF_NORMED) #เทียบรูป
        #TODO print(f"ค่าของการนำรูปไปเทียบจะแสดงผลออกมาเป็น numpy arry {result}") #แสดงผลการเทียบรูป
        
        #การรับค่าของตัวแปรที่ผ่าน method จะต้องเขียนให้ตัวแปรอยู่หน้าแล้ว method หรือ function 
        #อยู่หลังที่เสมือนเป็นค่าต่างๆที่เราต้องการจะเก็บไว้ในตัวแปร ก่อนจะเขียนลองรัน method นั้นๆว่าค่าที่แสดงมีออกมาเป็นอย่างไร จะได้สร้างตัวแปรรองรับถูกต้อง
        minval,maxval,minloc,maxloc = cv.minMaxLoc(result) #นำผลของการเทียบรูปมาเก็บไว้ในตัวแปรผ่าน method cv.minMaxLoc

        #print(f"ค่าความแม่นยําที่เกิดจากการเอาไปเทียบ {maxval}") #แสดงค่าความแม่นยํา
        #print(f"ตําแหน่ง [top left] ของรูปย่อย {maxloc}") #แสดงตําแหน่ง [top left] ของ รูปย่อยที่เราจะเอาไปเทียบ

        #threshold = 0.88 #ค่าเฉลี่ยที่เราจะใช้เป็นตัวอ้างอิงของความแม่นยํา
        
        locations = np.where(result >= threshold) #หาตำแหน่งที่เทียบเข้ากับค่าความแม่นยำ
        #print(f"ค่าหลังจากเอารูปที่เทียบที่มีค่าความแม่นยำแล้วแสดงตำแหน่งทั้งหมด {locations}") #แสดงตําแหน่งที่เทียบเข้ากับค่าความแม่นยำ
        locations = list(zip(*locations[::-1])) #แปลงข้อมูลเป็นรูปแบบ list โดยจัดแบ่งข้อมูลเป็น 2 มิติมีค่าแกน x และ y
        #print(f"ค่าตำแหน่งทั้งหมดหลังจากที่แปลงเป็น list {locations}")
        
        rectangles = [] #สร้างตัวแปรว่างรูปย่อยแบบ list เพื่อไว้สำหรับจัดการค่าที่ซ้ำ
        for loc in locations: #ทำการลูป locations ลงตัวแปร loc
            rect = [int(loc[0]),int(loc[1]),int(self.tempimg.shape[1]),int(self.tempimg.shape[0])] #จัดเรียงตำแหน่งของรูป x,y ที่เจอ แล้วเพิ่ม width, height ของรูปย่อยไปด้วย
            rectangles.append(rect) #เอา rect มาเก็บไว้ในตัวแปร
            rectangles.append(rect) #ทำซ้ำ
        #print(f"ค่าที่ผ่านการแปลงโดยloopที่ยังมีค่าซ้ำซ้อน{rectangles}") #แสดงตำแหน่งของรูปย่อยที่เราเก็บไว้ในตัวแปร
        
        point = [] #สร้างตัวแปรว่างรูปย่อยแบบ list เพื่อไว้รับค่ากึ่งกลางของรูป
        rectangles,weigts = cv.groupRectangles(rectangles,groupThreshold=1,eps=0.5) #จัดการข้อมูลที่ซ้ำซ้อนโดนผ่าน method cv.groupRectangles
        #print(f"ค่าที่ผ่านการจัดการค่าที่ซ้ำซ้อนแต่ยังเป็น numpy arry อยู่ {rectangles}") #แสดงตำแหน่งของรูปย่อยที่เราเก็บไว้ในตัวแปร
        
        if len(rectangles) > 0:
            for (x,y,w,h) in rectangles: #ทำการลูป rectangles ลงตัวแปร (x,y,w,h)
                #print(f"ค่าตำแหน่งรูป Top Left พร้อมขนาดของรูปย่อยที่ใช้เทียบ {x} {y} {w} {h}") #แสดงค่าของตำแหน่งของรูป
                top_left = (x,y) #เอา x และ y มาเก็บไว้ในตัวแปร
                bottom_right = (x + w,y + h) #เอา x + w และ y + h มาเก็บไว้ในตัวแปร bottom_right เพื่อเอาไปเปรียบเทียบกับรูปหลักในการหาจุดขวาล่างของรูป
                #หาตรงกลางของรูปโดยค่า x y หลังจากที่ผ่านการเปรียบเทียบแล้ว 
                center = (int(x + (w/2)),int(y + (h/2))) #เอา x + (w/2) และ y + (h/2) มาเก็บไว้ในตัวแปร center
                point.append(center) #เอา center มาเก็บไว้ในตัวแปร
                if debug: #เมื่อเปิด debug จะแสดงตำแหน่งของรูปย่อยที่เราเก็บไว้ในตัวแปร
                    print(f"ค่าตำแหน่งตรงกลางของรูป {center}")
                    cv.rectangle(self.mainimg,top_left,bottom_right,color=(0,255,0),thickness=1,lineType=cv.LINE_AA) #วาดกรอบลงรูปหลักที่คนหาเจอ
                    cv.putText(self.mainimg,txt,(top_left[0]-10,top_left[1]-5),cv.FONT_HERSHEY_SIMPLEX,0.5,color=(25,25,255),thickness=1,lineType=cv.LINE_AA)
                    cv.drawMarker(self.mainimg,center,color=(0,0,255),markerType=cv.MARKER_CROSS,markerSize=5,thickness=1,line_type=cv.LINE_AA) #วาดCrossตรงกลางของรูป
        else:
            print("No picture found") #แสดงข้อความเมื่อไม่มีรูปย่อย
              
        return point