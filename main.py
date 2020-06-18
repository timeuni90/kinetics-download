
import pandas as pd
from download import download_videos

if __name__ == '__main__':
    num_start = 100
    max_num_threading = 4
    data_frame = pd.read_csv(
        "./data/kinetics-400_train.csv",
        header=None,
        sep=","
    )
    videos_id_list = data_frame[1].tolist()[1:]
    labels = data_frame[0].tolist()[1:]
    start_time_list = data_frame[2].tolist()[1:]
    end_time_list = data_frame[3].tolist()[1:]
    download_videos(labels, videos_id_list,
                    "https://www.youtube.com/watch?v=",
                    start_time_list, end_time_list, num_start, max_num_threading)