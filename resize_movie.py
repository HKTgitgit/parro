#動画をリサイズし保存
import cv2

#パラメーター
resize = 4

#VideoCapture オブジェクトを取得
cap = cv2.VideoCapture("/home/kotetsu/デスクトップ/drone_code/common/data/video/cut/video_2_25_30.MP4")

#動画のプロパティを取得
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)
#書き出し設定
fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
writer = cv2.VideoWriter('/home/kotetsu/デスクトップ/drone_code/common/data/video/resize/video_2_25_30.MP4',fourcc, fps, (int(width/resize), int(height/resize)))

while True:
    ret, frame = cap.read()
    if not ret:
        break
    frame = cv2.resize(frame,(int(width/resize), int(height/resize)))
    writer.write(frame)

writer.release()
cap.release()