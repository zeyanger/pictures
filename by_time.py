#！/usr/bin/env.python
# _*_ coding:utf-8 _*_

import os
import stat
import time
import shutil
import piexif


def get_exifdate(filename):
    """获取GPSDATESTAMP"""
    data_dic = piexif.load(filename)
    if 29 in data_dic["GPS"].keys():
        # get GPSDateStamp
        date_get = data_dic['GPS'][29].decode('utf-8')
        return date_get.replace(':', '-')
    else:
        print('{}不包含GPS时间信息'.format(os.path.basename(filename)))


def get_mtime(filename):
    """获取文件修改时间"""
    file_state = os.stat(filename)
    mtime = time.localtime(file_state.st_mtime)
    date_y_m = str(mtime.tm_year) + '-' + str(mtime.tm_mon)
    return date_y_m


def show_file_properties(path):
    """show file properties, include path, size, creating time, change time"""
    # traverse all files
    for root, dirs, files in os.walk(path):
        print('位置:' + root)
        print(files)
        for file in files:
            file_path = os.path.join(root, file)
            f, e = os.path.splitext(file_path)
            if e.lower() not in ('.jpg', '.png', '.mp4', '.jpeg', '.bmp', '.tif', '.gif', '.3gp'):
                continue

            # get time
            date = get_exifdate(file_path)
            if not date:
                date = get_mtime(file_path)

            pwd = os.path.join(root, date)
            # 按日期重命名文件
            if not os.path.exists(pwd):
                new_filename = str(date + e)
            else:
                i = len(os.listdir(pwd))
                new_filename = str(str(date) + '(' + str(i + 1) + ')' + e)

            new_filepath = os.path.join(root, new_filename)
            os.rename(file_path, new_filepath)

            # 按照图片的拍摄日期创建目录，把每个图片放到相应的目录中去
            if not os.path.exists(pwd):
                os.mkdir(pwd)
                # 用copy2会保留图片的原始属性
            shutil.move(new_filepath, pwd)
            # os.remove(filename)


if __name__ == '__main__':
    show_file_properties('D:/读取照片信息并分类/WeiXin')
