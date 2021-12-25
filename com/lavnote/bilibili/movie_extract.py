# 扫描的根目录
import json
import logging
import os

import shutil

# 扫描的根目录
_source_root_path = "D:\\学习"
# 转换后的文件/文件夹根目录
_target_root_path = "D:\\前端"

logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")


def main():
    """
    获取视频文件信息，并转换重命名视频文件，复制到指定目录

    :return:
    """
    if not os.path.exists(_source_root_path):
        return
    for title_path_name in os.listdir(_source_root_path):
        movie_category(title_path_name)


def movie_category(title_path_name):
    """
    视频目录分类处理

    :param title_path_name: 视频目录分类名称
    :return:
    """
    title_path = os.path.join(_source_root_path, title_path_name)
    if not os.path.exists(title_path):
        return
    title_file_dir = os.path.join(title_path, '{}.dvi'.format(title_path_name))
    if not os.path.exists(title_file_dir):
        return
    # 获取标题所在文件
    title_file = open(title_file_dir)
    # 创建保存转换后的视频目录
    new_title_path = create_movie_title_dir(title_file.name)
    # 提取视频文件
    extract_movie(title_path, title_path_name, new_title_path)


def extract_movie(title_path, title_path_name, new_title_path):
    """
    提取视频文件

    :param title_path: 视频文件所在根目录
    :param title_path_name: 标题分类名称
    :param new_title_path: 新视频文件存放路径
    :return:
    """
    logging.info(title_path)
    movie_list_str = os.listdir(title_path)
    # 按数字大小顺序，排序视频文件名称列表
    movie_list = sorted(list(map(int, filter(lambda x: x.isdigit(), movie_list_str))))
    # 逐个处理视频文件
    for movie_dir_name in movie_list:
        # 视频文件目录
        movie_dir = os.path.join(title_path, str(movie_dir_name))
        # 视频文件名称路径信息
        movie_title_file_dir = os.path.join(movie_dir, "{}.info".format(title_path_name))
        if not os.path.exists(movie_title_file_dir):
            continue
        with open(file=movie_title_file_dir, mode='r', encoding='utf-8') as movie_title_file:
            movie_file_name = json.loads(movie_title_file.read())['PartName']
            movie_file_name = '{}-{}'.format(movie_dir_name, movie_file_name)

        # 视频文件路径
        source_movie_file_name = "{}_{}_0".format(title_path_name, movie_dir_name)
        file_ext_name = ''
        for path, path_names, file_names in os.walk(movie_dir):
            if path is not movie_dir:
                continue
            for file_name_tmp in file_names:
                file_ext_name = file_ext_name if source_movie_file_name not in file_name_tmp \
                                                 and 'video' not in file_name_tmp else file_name_tmp

        file_ext_name_sub = file_ext_name.split('.')[1]
        if source_movie_file_name not in file_ext_name.split('.')[0]:
            source_movie_file_dir = os.path.join(movie_dir, file_ext_name)
        else:
            source_movie_file_dir = os.path.join(movie_dir,
                                                 '{}.{}'.format(source_movie_file_name, file_ext_name_sub))
        logging.debug(source_movie_file_dir)
        logging.debug(os.path.join(new_title_path, '{}.{}'.format(movie_file_name, file_ext_name_sub)))
        shutil.copyfile(source_movie_file_dir,
                        os.path.join(new_title_path, '{}.{}'.format(movie_file_name, file_ext_name_sub)))


def create_movie_title_dir(title_file_name):
    """
    创建保存转换后的视频目录

    :param title_file_name: 标题名
    :return:
    """
    with open(file=title_file_name, mode='r', encoding='utf-8') as title_file:
        # 获取标题
        title_json = json.loads(title_file.read())
        new_title_path = os.path.join(_target_root_path, title_json['Title']).replace('/', '-')
        if not os.path.exists(new_title_path):
            os.makedirs(new_title_path)
    return new_title_path


if __name__ == '__main__':
    main()
