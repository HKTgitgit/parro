#動画を切り抜く
import cv2
import math
 
## 動画を開始ミリ秒～終了ミリ秒までカットする
## 
def trimVideo(targetFileName, destFileName, startMillis, stopMillis):
    ## FPS、フレーム数・開始終了フレーム番号取得
    videoCapture = cv2.VideoCapture(targetFileName)
    fps = videoCapture.get(cv2.CAP_PROP_FPS)
    totalFrames = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
    startFrameIndex = math.ceil(fps * startMillis / 1000)
    stopFrameIndex = math.ceil(fps * stopMillis / 1000)
    if(startFrameIndex < 0): 
        startFrameIndex = 0
    if(stopFrameIndex >= totalFrames):
        stopFrameIndex = totalFrames-1
    videoCapture.set(cv2.CAP_PROP_POS_FRAMES, startFrameIndex)
    frameIndex = startFrameIndex
    
    ## 開始～終了地点までフレーム分割
    imgArr = []
    while(frameIndex <= stopFrameIndex):
        _,img = videoCapture.read()
        imgArr.append(img)
        frameIndex += 1
        
    ## 分割フレームをmp4動画に再構成
    fourcc = cv2.VideoWriter_fourcc('m','p','4','v')
    video = None
    tmpVideoFileName = destFileName
    for img in imgArr:
        # re_size = 4
        # img = cv2.resize(img, dsize=(int(w/re_size), int(h/re_size)))
        if(video is None):
            h,w,_ = img.shape
            # img = cv2.resize(img, dsize=(int(w/re_size), int(h/re_size)))
            
            video = cv2.VideoWriter(tmpVideoFileName, fourcc, 20.0, (int(w),int(h)))
        video.write(img)
    video.release()
    
 
if __name__ == "__main__":
    ## こういう風に使う
    trimVideo(
        "/home/デスクトップ/drone_code/common/data/video/video//video_2.MP4",
        "/home/デスクトップ/drone_code/common/data/video/cut/video_2_40_45.MP4",
        3.2*1000,   ## => 3.2秒から
        12.8*1000  ## => 12.8秒まで
    )
