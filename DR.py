import cv2
import numpy as np
cap = cv2.VideoCapture(0)

dictionary_name = cv2.aruco.DICT_6X6_250
dictionary = cv2.aruco.getPredefinedDictionary(dictionary_name)
marker = cv2.aruco.drawMarker(dictionary, 2, 400)
cv2.imwrite("aucotest.png", marker)

planeImg = []
x_bias = 50
y_bias = 50

bias = 10

original_points = np.float32([[320 - x_bias, 240 - y_bias], [320 + x_bias, 240 - y_bias], 
                              [320 + x_bias, 240 + y_bias], [320 - x_bias, 240 + y_bias]])

def trans_points(point1):
    print(point1)


def diminished_trans(planeImg, markerImg, marker_region, detected_marker_region, dictionary):
    H = cv2.getPerspectiveTransform(detected_marker_region, original_points)
    markerImg2 = cv2.warpPerspective(markerImg , H, (640, 480))
    markerImg2[240 - y_bias - bias:240 + y_bias + bias, 320 - x_bias - bias:320 + x_bias + bias] = planeImg[240 - y_bias - bias:240 + y_bias + bias, 320 - x_bias - bias:320 + x_bias + bias]
    H2 = cv2.getPerspectiveTransform(original_points, detected_marker_region)
    markerImg3 = cv2.warpPerspective(markerImg2 , H2, (640, 480))
    return markerImg2, markerImg3
    
    


# 何もないときの写真を撮影
while True:
    ret, frame = cap.read()
    
    cv2.imshow('Edited Frame', frame)
    k = cv2.waitKey(1)
    #aが入力されたとき
    if k == 97:
        planeImg = frame
        break

cv2.destroyAllWindows()
#マーカを置いたときの写真を撮影
marker_region = 0

while True:
    ret, frame = cap.read()
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, dictionary)
    frame2 = cv2.aruco.drawDetectedMarkers(frame, corners, ids)
    cv2.imshow('Edited Frame', frame2)
    k = cv2.waitKey(1)
    #bが入力されたとき
    if k == 98 and ids != None:        
        marker_region = corners[0]
        break

H1 = cv2.getPerspectiveTransform(marker_region, original_points)
planeImg = cv2.warpPerspective(planeImg , H1, (640, 480))
cv2.imwrite("test2.png", planeImg)

print(marker_region[0])
cv2.destroyAllWindows()

while True:
    ret, frame = cap.read()

    # スクリーンショットを撮りたい関係で1/3サイズに縮小
    #frame = cv2.resize(frame)

    # ArUcoの処理 corners:　検出されたマーカの座標, ids：　検出されたマーカーのid
    corners, ids, rejectedImgPoints = cv2.aruco.detectMarkers(frame, dictionary)
    #frame = cv2.aruco.drawDetectedMarkers(frame, corners, ids)
    
    #cornersがNoneじゃないときに射影変換
    if (ids != None):
        #print(corners[0])
        marker1, marker2 = diminished_trans(planeImg, frame, marker_region[0], corners[0], dictionary)
        cv2.imshow('Edited Frame1', marker1)
        cv2.imshow('Edited Frame2', marker2)
        #cornersの座標格納順は，左上右上右下左下
#        trans_points = np.float32([[170,90], [470, 90], [470, 390], [170, 390]])
#        H = cv2.getPerspectiveTransform(corners[0], trans_points)
#        frame = cv2.warpPerspective(frame , H, (640, 480))
        

    # 加工済の画像を表示する
    cv2.imshow('Edited Frame', frame)

    # キー入力を1ms待って、k が27（ESC）だったらBreakする
    k = cv2.waitKey(1)
    if k == 27:
        break

cap.release()
cv2.destroyAllWindows()