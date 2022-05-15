import os
import sys
from multiprocessing import Pool

def work(movie_path):
    os.chdir(movie_path)
    unzip_path = "auto_unziped_files"
    if os.path.exists(unzip_path):
        print(f"已经存在tmp目录，请确认是否覆盖！{movie_path}")
        return 0
    cmd = f'WinRAR x "*.rar" {unzip_path}/'
    print(cmd)
    os.system(cmd) 
    return 0


def unzip_all(input_movie_path):
    real_movie_path_list = []

    for root, dirs, files in os.walk(input_movie_path, topdown=False):
        for d in dirs:
            folder_path = os.path.join(root, d)
            for i in os.listdir(folder_path):
                if "rar" in i:
                    real_movie_path_list.append(folder_path)
                    break

    print(real_movie_path_list)   

    p = Pool(10)
    res_1 = []
    for i in real_movie_path_list:
        res = p.apply_async(work,args=(i,))
        res_1.append(res)    
    p.close()
    p.join()

    for res in res_1:
        print(res.get())

def get_possible_better_movie_name(file_path, input_movie_path):
    #print(f"get_possible_better_movie_name:{file_path}, {input_movie_path}")
    if os.path.isfile(file_path):
        parent_folder_path = os.path.dirname(file_path)

        # 文件名不带后缀
        file_name_no_postfix = os.path.basename(file_path)
        file_name_no_postfix = os.path.splitext(file_name_no_postfix)[0]

        tmp_path = os.path.join(parent_folder_path, file_name_no_postfix)
    else:
        tmp_path = file_path
    
    tmp_path = tmp_path.replace("\\", "/")
    input_movie_path = input_movie_path.replace("\\", "/")
    tmp_path = tmp_path.replace(input_movie_path, "")
    folder_list = tmp_path.split("/")

    for i in folder_list:
        folder_name = i.lower()
        if "bdrip" in folder_name or "2160p" in folder_name or "bluray" in folder_name or "atmos" in folder_name or "5.1" in folder_name or "7.1" in folder_name:
            return i

    # 取文件名为目录名
    for i in folder_list:
        if len(i) > 0:
            return i
    
    sys.exit(1)

def make_copy_scirpt(input_movie_path, dst_path):
    bat_content = []
    bat_content.append(f"set dst_path={dst_path}")
    for root, dirs, files in os.walk(input_movie_path, topdown=False):
        for d in dirs:
            folder_path = os.path.join(root, d)
            #print(f"ddd:{d}")
            if str(d).lower() == "bdmv":
                dst_folder_name = get_possible_better_movie_name(folder_path, input_movie_path)
                bat_content.append(f'md "%dst_path%/{dst_folder_name}"')
                cmd = f'xcopy /S /Y "{os.path.dirname(folder_path)}/*" "%dst_path%/{dst_folder_name}"'
                bat_content.append(cmd)
        for f in files:
            file_path = os.path.join(root, f)
            if str(f).endswith(".iso") or str(f).endswith(".mkv"):
                if os.stat(file_path).st_size > 0: # 1024*1024*1024:
                    dst_folder_name = get_possible_better_movie_name(file_path, input_movie_path)
                    bat_content.append(f'md "%dst_path%/{dst_folder_name}"')
                    cmd = f'xcopy /S /Y "{file_path}" "%dst_path%/{dst_folder_name}"'
                    bat_content.append(cmd)
                else:
                    print(f"[WARNING]发现小于1G的视频文件：{file_path}")

    with open(os.path.join(input_movie_path, "copy_movie.bat"), "w", encoding='gbk') as f:
        f.write("\n".join(bat_content))
    print("\n".join(bat_content))

def main():
    #input_movie_path = sys.argv[1]
    input_movie_path = r"H:\develop\unzip_movie\test_movie"
    dst_path = r"h:\haha\haha2"
    #unzip_all(input_movie_path)
    make_copy_scirpt(input_movie_path, dst_path)
    

if __name__ == '__main__':
    main()