import cv2
def match_template(image_path, template_path):
    screen = cv2.imread(image_path)
    template = cv2.imread(template_path)
    try:
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    except Exception :
        return -1,-1,-1
        
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc
    bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
    center=((top_left[0]+bottom_right[0])/2,(top_left[1]+bottom_right[1])/2)
#     cv2.rectangle(screen,top_left, bottom_right,(0,0,255),3)
#     cv2.imshow("imgRec",screen)
    
       
    #x,y相反  --（y,x）
    
    
    print(template_path,center)
    return top_left,bottom_right,max_val
def isMatch(Tmplatepath,confid):
    top_left,bottom_right,max_val= match_template('screenshot.png', Tmplatepath)
    if max_val>confid:
        print(Tmplatepath,max_val)
        return max_val
    else:
        return 0
def match_template_EX(image_path, template_path):
    screen = cv2.imread(image_path)
    template = cv2.imread(template_path)
    try:
        result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)
    except Exception :
        return -1,-1,-1
        
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
    top_left = max_loc
    bottom_right = (top_left[0] + template.shape[1], top_left[1] + template.shape[0])
    center=((top_left[0]+bottom_right[0])/2,(top_left[1]+bottom_right[1])/2)
    cv2.rectangle(screen,top_left, bottom_right,(0,0,255),3)
    cv2.imshow("imgRec",screen)
    
       
    #x,y相反  --（y,x）
    
    
    print(template_path,center)
    return top_left,bottom_right,max_val