
import subprocess
import logging
import pandas as pd
import os

def get_logger(log_name, logging_level):
    logger = logging.getLogger(log_name)
    logger.setLevel(logging_level)
    handler = logging.FileHandler(log_name)
    handler.setLevel(logging_level)
    formatter = logging.Formatter('%(asctime)s - %(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger

error_download_filename = "./log/error_download.log"
success_download_filename = "./log/success_download.log"
error_trim_filename = "./log/error_trim.log"
success_trim_filename = "./log/success_trim.log"
if not os.path.exists('./log'):
    os.makedirs("./log")
error_download_logger = get_logger(error_download_filename, logging.ERROR)
success_download_logger = get_logger(success_download_filename, logging.DEBUG)
error_trim_logger = get_logger(error_trim_filename, logging.ERROR)
success_trim_logger = get_logger(success_trim_filename, logging.DEBUG)

def download_video(num, url, video_id, output_filename,
                   tmp_filename, start_time, end_time):
    # 下载视频
    command = [
        "youtube-dl",
        "-f", "worstvideo/worst",
        "-o", tmp_filename,
        url
    ]
    command = " ".join(command)
    output = subprocess.run(command, shell=True, stderr=subprocess.PIPE)
    if output.returncode != 0:
        message = "{} - {} - {}".format(num, video_id, output.stderr)
        error_download_logger.error(message)
        return
    success_download_logger.debug("{} - {}".format(num, video_id))
    # 裁剪视频
    command = ['ffmpeg',
               '-i', '"%s"' % tmp_filename,
               '-ss', str(start_time),
               '-t', str(end_time - start_time),
               '-c:v', 'libx264', '-c:a', 'copy',
               '-threads', '1',
               '-loglevel', 'panic',
               '"%s"' % output_filename]
    command = ' '.join(command)
    output = subprocess.run(command, shell=True, stderr=subprocess.PIPE)
    if output.returncode != 0:
        message = "{} - {} - {}".format(num, video_id, output.stderr)
        error_trim_logger.error(message)
        return
    success_trim_logger.debug("{} - {}".format(num, video_id))

def download_videos(labels, video_id_list, url_base, start_time_list, end_time_list):
    length = len(video_id_list)
    for i in range(length):
        print("--------------------{}---------------------".format(i))
        url = url_base + video_id_list[i]
        output_filename = "./dataset/{}/{}.mp4".format(labels[i], video_id_list[i])
        tmp_filename = "./tmp/{}/{}.mp4".format(labels[i], video_id_list[i])
        print("download - {}/{}".format(i, length))
        if not os.path.exists('./dataset/{}'.format(labels[i])):
            os.makedirs('./dataset/{}'.format(labels[i]))
        download_video(i, url, video_id_list[i], output_filename,
                       tmp_filename, int(start_time_list[i]), int(end_time_list[i]))

if __name__ == '__main__':
    data_frame = pd.read_csv(
        "./data/kinetics-400_train.csv",
        header=None,
        sep=","
    )
    videos_id_list = data_frame[1].tolist()[1:]
    labels = data_frame[0].tolist()[1:]
    start_time_list = data_frame[2].tolist()[1:]
    end_time_list = data_frame[3].tolist()[1:]
    download_videos(labels, videos_id_list, "https://www.youtube.com/watch?v=", start_time_list, end_time_list)