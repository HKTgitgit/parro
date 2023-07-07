import cv2
import os

def save_frame_range_sec(video_path, dir_path, basename,
						 start_sec=0, stop_sec=100, step_sec=1,
						  ext='jpg'):
	cap = cv2.VideoCapture(video_path)
	print("ビデオの読み込み完了")
	if not cap.isOpened():
		print("videoがありません")
		return

	os.makedirs(dir_path, exist_ok=True)
	base_path = os.path.join(dir_path, basename)

	digit = len(str(int(cap.get(cv2.CAP_PROP_FRAME_COUNT))))    #総フレーム数

	fps = cap.get(cv2.CAP_PROP_FPS) #1秒あたりのフレーム数
	fps_inv = 1 / fps

	sec = start_sec
	i = 0
	while sec < stop_sec:
		i += 1
		n = round(fps * sec)
		cap.set(cv2.CAP_PROP_POS_FRAMES, n)
		ret, frame = cap.read()
		if ret:\
			cv2.imwrite(
				f'{base_path}_{i}.{ext}', frame)
		   
		else:
			print("完了")
			return
		sec += step_sec

start = 10
end = 2100
step = 2.5
save_frame_range_sec('/home/kotetsu/デスクトップ/drone_code/common/data/video/video_2/resize/resized_video_2.MP4',  #vido path
					 '/home/kotetsu/デスクトップ/drone_code/common/data/video/test',  #save path
					 '5m',            #save name
					 start_sec=start, stop_sec=end, step_sec=step,)     #star stop step