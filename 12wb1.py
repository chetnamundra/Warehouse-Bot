import cv2
import numpy as np
import math as mt

"""
variable listing ---

img1- first image with only nodes and lines
img2- second image with area segregation
img3- third image with package locations

nc= list of coordinates of nodes
[[x,y],[x,y]..]

ncc= list of node number which forms a line and its distance
[[node 1, node 2, distance],...]

d= dictionary based on every node(all the possible nodes connected to key node and its distance)
ex
{0 : [[1, 129], [2, 61], [7, 389]], 1:[...}

hcd= dictinary based on all areas and nodes inside that area
mf- manufacturing unit (red)
do- drop off area(yellow)
ca- collection area (green)
da- distriibution area (blue)
(hcd- hard coded disctionary which was supposed to be hardcoded but isnt hardcoded anymore)
#hcd={"mf":{34:"",30:"",16:"",14:"",5:"",3:""},"do":{17:"",18:"",31:""},"ca":{32:"",33:"",19:"",20:""},"da":{11:"",8:"",2:""}}
empty strings change to color red, green or blue if its near one of locations

start- yellow- location from where bot starts


ppl
(path planning list)- list made from dictionary hcd deciding the pick up and drop off all packages from start till start

newh= final list giving all the directions that bot needs, to be connected with bluetooth

em= decided wether electromagnet of bot should be on or off

functions-

getNodes- to get all the corrdinate of nodes

getLinePeri- to get all the lines and its perimeter

clrDetectfordict- color detection for areas

clrDetect- color detection for location of packages drop off and pick up locations

pp- path planning (plans shortest route and returns directions:

    path- gives shortest route in it:

         w= list of shortest route
         c1= shortest distance amongst all routes
         p= all the possible paths from ori to des
         ori= origin
         des= destination
         c= distance of the possible path
         dd= same as but to remove all the duplication of paths

    slope- gives slope of line ([x,y],[x,y])
    
    lfp- gives consntants of a line ([x,y],[x,y])
    
    ab2l(angle between 2 lines)-
    returns straight or left or right for all normal conditions

    c for curve line condition

    
process---

1> identify nodes

2> identify lines connecting which all nodes and length of line

3> identify different areas using color detection

4> identify package drop off and pick location nodes + start location

5> find the shortes route for every node to node

6> give directions to bot acc to the shortest selected path
    

for bluetooth connection

L- turn left and move forward
R- turn right and move forward
U- take a u-turn and move forward
S- keep going straight
P- stop and switch on electromagnet(keep it on)
D- stop and switch off electromangnet(keep it off)

"""

def getNodes(img):

    def getContours(img):
        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            #cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 2)
            peri = cv2.arcLength(cnt, True)
            #print(int(peri/2))
            #dist=str(int(peri/2))
            approx = cv2.approxPolyDP(cnt, 0.0000000002 * peri, True)
            #print(len(approx))
            objCor = approx
            #print(objCor)
            x, y, w, h = cv2.boundingRect(approx)

            #cv2.putText(imgContour, dist,(x + (w // 2) - 10, y + (h // 2) - 10), cv2.FONT_HERSHEY_COMPLEX, 0.7,(0, 0, 0), 2)
            
        nc=getCentre(contours,img)
        return nc

    def getCentre(cnts,img):
        nc=[]
        i=0
        for c in cnts:

            M = cv2.moments(c)
            try:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            except ZeroDivisionError:
                print("Division by Zero!")
            ctr=(cX,cY)
            #print(ctr)
            nc.append([cX,cY])
            cv2.circle(img1, ctr, 10,(0,255,0),2)
            cv2.circle(imgContour2, ctr, 12,(255, 255, 255), -1)

            #cv2.putText(img1, str(i),(cX + 20,cY + 20), cv2.FONT_HERSHEY_COMPLEX, 0.5, 0, 1)
            i+=1
        return nc
            

    nc=getContours(img)
    return nc

def getLinePeri(img,nc):
    
    def getContours(img,nc):
        d={}
        ncc=[]
        contours, hierarchy = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
        for cnt in contours:
            #cv2.drawContours(imgContour, cnt, -1, (255, 0, 0), 2)
            peri = cv2.arcLength(cnt, True)
            #print(int(peri/2))
            dist=str(int(peri/2))
            approx = cv2.approxPolyDP(cnt, 0.0000000002 * peri, True)
            #print(len(approx))
            s=0.5
            x1=approx[0][0][0]
            y1=approx[0][0][1]
            x2=approx[int(s*len(approx))][0][0]
            y2=approx[int(s*len(approx))][0][1]
            
            
            #print(nc1)
            if mt.dist([x1,y1],[x2,y2])>20:
                for i in range(0,len(nc)):
                    
                    
                    for j in range(i+1,len(nc)):
                        
                        
                        if (mt.dist(nc[i],[x1,y1])<30 and mt.dist(nc[j],[x2,y2])<30 ) or (mt.dist(nc[j],[x1,y1])<30 and mt.dist(nc[i],[x2,y2])<30):
                            
                            cv2.line (img1, (nc[i][0], nc[i][1]), (nc[j][0], nc[j][1]), (0,255,0), 2)
                            if [i,j,int(dist)] not in ncc:
                                ncc.append([i,j,int(dist)])
                        else:
                            for s in range(45,56):
                                s=s/100
                                x2=approx[int(s*len(approx))][0][0]
                                y2=approx[int(s*len(approx))][0][1]
                                if (mt.dist(nc[i],[x1,y1])<30 and mt.dist(nc[j],[x2,y2])<30 ) or (mt.dist(nc[j],[x1,y1])<30 and mt.dist(nc[i],[x2,y2])<30):
                            
                                    cv2.line (img1, (nc[i][0], nc[i][1]), (nc[j][0], nc[j][1]), (0,255,0), 2)
                                    if [i,j,int(dist)] not in ncc:
                                        ncc.append([i,j,int(dist)])

                            
            objCor = approx
            #print(objCor)
            x, y, w, h = cv2.boundingRect(approx)

            #cv2.putText(img1, dist,(x + (w // 2) + 20, y + (h // 2) + 20), cv2.FONT_HERSHEY_COMPLEX, 0.5,(0, 0, 0), 1)
        #print(ncc)
        #print(len(ncc))
        #getCentre(contours,img)
        return ncc

    def getCentre(cnts,img):
        i = 0
        for c in cnts:

            M = cv2.moments(c)
            try:
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
            except ZeroDivisionError:
                print("Division by Zero!")
            ctr=(cX,cY)
            #print(ctr)
            #cv2.circle(imgContour, ctr, 2, (255, 255, 255), -1)
            #cv2.circle(imgContour2, ctr, 12,(255, 255, 255), -1)
            

            #cv2.putText(imgContour, str(i),(cX + 20,cY + 20), cv2.FONT_HERSHEY_COMPLEX, 0.7,(0, 255, 0), 2)
            i=i+1
            
    ncc=getContours(img,nc)
    return ncc
    
    

img1 = cv2.imread(r"C:\Users\Chetna\OneDrive\Pictures\Saved Pictures\hd.jpg")
imgContour = img1.copy()
imgContour2 = img1.copy()
kernel = np.ones((5,5),np.uint8)

imgGray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
imgBlur = cv2.GaussianBlur(imgGray, (7, 7), 1)
imgDia = cv2.dilate(imgBlur,kernel,iterations=3)
imgCanny = cv2.Canny(imgDia, 50, 50)
imgDialate = cv2.dilate(imgCanny,kernel,iterations=2)

nc=getNodes(imgDialate)

#print(nc)

imgBlank = np.zeros_like(img1)

#cv2.imshow("nodes",imgContour)
#cv2.imshow("new",imgContour2)

imgBlur2 = cv2.GaussianBlur(imgContour2, (7,7), 1)
imgDia2 = cv2.dilate(imgBlur2,kernel,iterations=1)
imgCanny2 = cv2.Canny(imgDia2, 70,70)
imgDialate2 = cv2.dilate(imgCanny2,kernel,iterations=1)


ncc=getLinePeri(imgDialate2,nc)

#print(ncc)

d={}
for i in range(len(nc)):
    
    l=[]
    for j in ncc:
        if i==j[0]:
            l.append([j[1],j[2]])
           
        elif i==j[1]:
            l.append([j[0],j[2]])
            
    d[i]=l

for i in d:
    #print(i ,":", d[i])
    pass



red_l = [169,100,100]
red_u = [189,255,255]
blue_l=[110,50,50]
blue_u=[130,255,255]
green_l=[50,20,20]
green_u=[100,255,255]
yellow_l=[20, 80, 80]
yellow_u=[30, 255, 255]

img2 = cv2.imread(r"C:\Users\Chetna\OneDrive\Pictures\Saved Pictures\hd4.png")



def clrDetectfordict(img,l,u,x) :
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # lower bound and upper bound for Green color
    lower_bound = np.array(l)
    upper_bound = np.array(u)
    # find the colors within the boundaries
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    kernel = np.ones((7,7),np.uint8)
    # Remove unnecessary noise from mask
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    segmented_img = cv2.bitwise_and(img, img, mask=mask)

    contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    output = cv2.drawContours(img, contours, -1, (0, 0, 0), 2)
    hcd[x]={}
    for cnt in contours:
        #print(cnt)
        for i in range(len(nc)):
            if cnt[0][0][0]<nc[i][0]<cnt[2][0][0] and cnt[0][0][1]<nc[i][1]<cnt[2][0][1]:
                hcd[x][i]=""
            

hcd={}
clrDetectfordict(img2,red_l,red_u,"mf")    
clrDetectfordict(img2,yellow_l,yellow_u,"do")
clrDetectfordict(img2,green_l,green_u,"ca")
clrDetectfordict(img2,blue_l,blue_u,"da")
#print(hcd)

#hcd={"mf":{34:"",30:"",16:"",14:"",5:"",3:""},"do":{17:"",18:"",31:""},"ca":{32:"",33:"",19:"",20:""},"da":{11:"",8:"",2:""}}
    
def clrDetect(img,l,u,x) :
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    # lower bound and upper bound for Green color
    lower_bound = np.array(l)
    upper_bound = np.array(u)
    # find the colors within the boundaries
    mask = cv2.inRange(hsv, lower_bound, upper_bound)

    kernel = np.ones((7,7),np.uint8)
    # Remove unnecessary noise from mask
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)

    segmented_img = cv2.bitwise_and(img, img, mask=mask)

    contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    output = cv2.drawContours(img, contours, -1, (0, 0, 0), 2)

    
        
    #find centre point using midpoint of diagonal
    for cnt in contours :
        #print(cnt[0][0])
        for i in range(len(nc)):
            if abs(cnt[0][0][0]-nc[i][0])<50 and abs(cnt[0][0][1]-nc[i][1])<50:
                if x=="yellow":
                    return i
                #print(i)
                for j in hcd:
                    for k in hcd[j]:
                        if k==i:
                            hcd[j][k]=x
                


img3 = cv2.imread(r"C:\Users\Chetna\OneDrive\Pictures\Saved Pictures\hd3.png")


clrDetect(img3,red_l,red_u,"red")
clrDetect(img3,green_l,green_u,"green")
clrDetect(img3,blue_l,blue_u,"blue")
start=clrDetect(img3,yellow_l,yellow_u,"yellow")


#print(start,hcd)

print(hcd)
ppl=[start]

clr=["red","green","blue"]
for j in clr:
    for i in hcd["mf"]:
        if hcd["mf"][i]==j:
            for k in hcd["do"]:
                if hcd["do"][k]==j:
                    ppl.append(i)
                    ppl.append(k)
                   
    for i in hcd["ca"]:
        if hcd["ca"][i]==j:
            for k in hcd["da"]:
                if hcd["da"][k]==j:
                    ppl.append(i)
                    ppl.append(k)


ppl.append(start)               
print(ppl)
hcd1={}
for i in hcd:
    hcd1[i]={}
    for j in hcd[i]:
        if hcd[i][j]=="":
            pass
        else:
            hcd1[i][j]=hcd[i][j]
print(hcd1)

def pp(ori,des,newh,d):
    
    c1=999999
    w=[]

    p=[[ori]]
    def path(p,c1,w=[]):
        
        
        
        x=[]
        x.extend(p)
        n=len(x)
        #print(x)
        for i in range(n):
            q=x[i][len(x[i])-1]
            
            bre=0
            
            #print(ori)
            for j in d:
                
                if j==q:
                    
                    for k in d[j]:
                        #print(k[0])
                        if k[0]==des:
                            m=[]
                            m.extend(x[i])
                            m.append(k[0])
                            c=0
                            for j in range(len(m)-1):
                                for k in d:
                                    if m[j]==k:
                                        for l in d[k]:
                                            if l[0]==m[j+1]:
                                                c+=l[1]
                            if c<c1:
                                w=m
                                c1=c
                            bre=1
                            break
                        else:
                            m=[]
                            m.extend(x[i])
                            #print(m)
                        
                            m.append(k[0])
                            p.append(m)
                            #print(m)
                    if bre==1:
                        break
                if bre==1:
                    
                    break
                                
            p.remove(x[i])
        
                

        dd=[]
        dd.extend(p)
        for ab in dd:
            for bc in range(len(ab)):
                if ab.count(ab[bc])>1:
                    
                    p.remove(ab)
                    break
        
        #print(p)
        if len(p)==0:
            #print(w)
            return w,c1
        
        w,c1=path(p,c1,w)
        return w,c1
       
    w,c1=path(p,c1,w)           

    

    #print(w,c1)
    
            

    def slope(l,n):
        if (l[0]-n[0])==0:
            return 999
        else:
        
            m=(l[1]-n[1])/(l[0]-n[0])
            return m

    def lfp(P, Q):
     
        a = Q[1] - P[1]
        b = P[0] - Q[0]
        c = a*(P[0]) + b*(P[1])
        return (a,b)

    def ab2l(m,n,o,p):
        a1,b1=lfp(m,n)
        a2,b2=lfp(o,p)
        
        if (a1*a2+b1*b2)==0:
            t=slope(m,p)
            
            if m[1]-n[1]>50 or n[1]-m[1]>50:
            
                if t>0:
                    return "L"
                else:
                    return "R"
            else:
                if t>0:
                    return "R"
                else:
                    return "L"
        
        t=mt.degrees(mt.atan((a2*b1-a1*b2)/(a1*a2+b1*b2)))

        #print(t,m,n,p)
            
        
            
        if -12<t<12:
            return "S"
        elif 75<t<105 or -75>t>-105:
            t=slope(m,p)
            #print(t)

            if m[1]-n[1]>50 or n[1]-m[1]>50:
            
                if t>0:
                    return "L"
                else:
                    return "R"
            else:
                if t>0:
                    return "R"
                else:
                    return "L"
        
        
            
        else:
            return "C"
            
            
    h=[]
    
    if w[0]==start:
        t=slope(nc[start],nc[w[1]])
        #print(t)
        if -12<t<12:
            h.append("S")
            
        elif t==999:
            h.append("L")
            
        else:
            h.append("R")
            
    i=0
    while i<(len(w)-2):
        #print(i)
        d=ab2l(nc[w[i]],nc[w[i+1]],nc[w[i+1]],nc[w[i+2]])
        #print(w[i],w[i+1],w[i+2],d)
        if d=="C":
            
            if slope(nc[w[i]],nc[w[i+1]])==1.0:
                t=slope(nc[w[i]],nc[w[i+2]])
                #print(t)
                if -1>t:
                    h.append("L")
                else:
                    h.append("R")
                i+=1
            elif slope(nc[w[i+1]],nc[w[i+2]])==1.0 :
                
                t=slope(nc[w[i]],nc[w[i+2]])
                #print(t)
                if nc[w[i]][1]-nc[w[i+1]][1]>50 or nc[w[i+1]][1]-nc[w[i]][1]>50:
                
                    if t>0:
                        h.append("L")
                    else:
                        h.append("R")
                else:
                    if t>0:
                        h.append("R")
                    else:
                        h.append("L")
                
                i+=1
            else:
                a=mt.dist(nc[w[i+1]],nc[w[i]])
                b=mt.dist(nc[w[i+2]],nc[w[i+1]])
                c=mt.dist(nc[w[i+2]],nc[w[i]])
                #print(a,b,c)
                d=mt.degrees(mt.acos((a**2+b**2-c**2)/(2*a*b)))
                #print(d)
                
                if d>90 or d<-90:
                    h.append("S")
                else:          
                    t=slope(nc[w[i]],nc[w[i+2]])
                    if nc[w[i]][1]-nc[w[i+1]][1]>50 or nc[w[i+1]][1]-nc[w[i]][1]>50:
                    
                        if t>0:
                            h.append("R")
                        else:
                            h.append("L")
                    else:
                        if t>0:
                            h.append("L")
                        else:
                            h.append("R")
                if i==(len(w)-3):
                    break
                
                a=mt.dist(nc[w[i+2]],nc[w[i+1]])
                b=mt.dist(nc[w[i+3]],nc[w[i+2]])
                c=mt.dist(nc[w[i+3]],nc[w[i+1]])
                #print(a,b,c)
                d=mt.degrees(mt.acos((a**2+b**2-c**2)/(2*a*b)))
                if d>90 or d<-90:
                    h.append("S")
                else:          
                    t=slope(nc[w[i+1]],nc[w[i+3]])
                    if nc[w[i+1]][1]-nc[w[i+2]][1]>50 or nc[w[i+2]][1]-nc[w[i+1]][1]>50:
                    
                        if t>0:
                            h.append("L")
                        else:
                            h.append("R")
                    else:
                        if t>0:
                            h.append("R")
                        else:
                            h.append("L")
                i+=2
        else:
            h.append(d)
            i+=1

    
                
             
    #print(h)
    return newh.extend(h)


newh=[]
em="D"

for i in range(len(ppl)-1):

    pp(ppl[i],ppl[i+1],newh,d)
    if em=="D":
        newh.append('P')
        
        em='P'
    else: 
        newh.append('D')
        
        em='D'

newh.pop(len(newh)-1)
newh.append('O')

print(newh)
    
#print("ok")


cv2.imshow("final",img1)
cv2.imshow("areas", img2)
cv2.imshow("package", img3)

cv2.waitKey(0)

