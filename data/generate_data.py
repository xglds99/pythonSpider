import os
import shutil
fold_path = "D:\ILSVRC2012\ILSVRC2012_img_train\ILSVRC2012_img_train"


def copy_image():
    copyfold_list = os.listdir(fold_path)
    for fold in copyfold_list:
        if fold.endswith(".tar"):
            continue
        fold_new = os.path.join(fold_path, "val", fold)
        os.makedirs(fold_new, exist_ok=True)
        image_cnt = 0
        image_name_list = os.listdir(os.path.join(fold_path,fold))
        for i in range(100,120):

        # for image_name in os.listdir(os.path.join(fold_path,fold)):
        #     if image_cnt > 20:
        #         break
                # 复制图片文件
            shutil.copy2(os.path.join(fold_path,fold,image_name_list[i]), os.path.join(fold_new,image_name_list[i]))
            image_cnt += 1
        print("fold" + fold + "finished!")

copy_image()