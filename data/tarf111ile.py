import os
import tarfile


def extract_tar_files(folder_path):
    # 遍历文件夹中的所有文件
    for file_name in os.listdir(folder_path):
        # 检查文件是否为.tar文件
        if file_name.endswith('.tar'):
            # 获取.tar文件的完整路径
            tar_file_path = os.path.join(folder_path, file_name)

            # 创建一个与.tar文件同名的文件夹来存放解压缩后的文件
            extracted_folder_path = os.path.join(folder_path, file_name[:-4])
            os.makedirs(extracted_folder_path, exist_ok=True)

            # 打开并解压.tar文件
            with tarfile.open(tar_file_path, 'r') as tar:
                tar.extractall(path=extracted_folder_path)
                print(f"Extracted {file_name} to {extracted_folder_path}")


# 使用你的文件夹路径替换下面的路径
folder_path = 'D:\ILSVRC2012\ILSVRC2012_img_train\ILSVRC2012_img_train'
extract_tar_files(folder_path)
