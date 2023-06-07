import os
import zipfile

# 定义要压缩的文件夹路径
folder_path = "./"

# 获取该文件夹下所有子文件夹的路径
sub_folders = [f.path for f in os.scandir(folder_path) if f.is_dir()]

# 遍历所有子文件夹，分别进行压缩
for sub_folder in sub_folders:
    # 构造压缩包名称
    zip_name = sub_folder + '.zip'

    # 创建zip文件对象
    zip_file = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)

    # 遍历该子文件夹下的所有文件和子文件夹，并添加到zip文件中
    for root, dirs, files in os.walk(sub_folder):
        for file in files:
            zip_file.write(os.path.join(root, file))
        for dir in dirs:
            zip_file.write(os.path.join(root, dir))

    # 关闭zip文件对象
    zip_file.close()

