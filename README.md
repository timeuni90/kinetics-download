# kinetics-download
kinetics 数据集下载程序，需要翻墙。下载的原始数据会放在 ./tmp 目录下，裁剪后的数据会放在 ./dataset 目录下，./log 目录下有 4 个日志记录文件：success_download.log、error_download.log、success_trim.log和error_trim.log，分别用来记录下载成功、下载失败、裁剪成功、裁剪失败的视频。
# 使用方法
1 安装依赖：pip install -r requirements.txt
2 运行 download.py 文件
