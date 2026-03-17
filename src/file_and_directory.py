import os
import shutil


def _copy_directory_contents(src, dst):
    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        dst_item = os.path.join(dst, item)

        if os.path.isfile(src_item):
            print(f"Copying file: {src_item} -> {dst_item}")
            shutil.copy(src_item, dst_item)
        else:
            os.mkdir(dst_item)
            _copy_directory_contents(src_item, dst_item)


def copy_directory_recursively(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)

    os.mkdir(dst)
    _copy_directory_contents(src, dst)