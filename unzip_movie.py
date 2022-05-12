import os
import sys

def main():
    print("haha")
    # WinRAR x "*.rar" tmp/
    real_movie_path_list = []
    #movie_path = sys.argv[1]
    movie_path = "H:/movie"
    for root, dirs, files in os.walk(movie_path, topdown=False):
        for d in dirs:
            folder_path = os.path.join(root, d)
            for i in os.listdir(folder_path):
                if "rar" in i:
                    real_movie_path_list.append(folder_path)
                    break

    print(real_movie_path_list)   
    for i in real_movie_path_list:
        os.chdir(i)
        cmd = 'WinRAR x "*.rar" tmp/'
        print(cmd)
        os.system(cmd)         

if __name__ == '__main__':
    main()