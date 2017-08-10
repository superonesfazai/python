# coding = utf-8

'''
@author = super_fazai
@File    : 简单的实现shell下类似cat的功能.py
@Time    : 2017/8/8 12:26
@connect : superonesfazai@gmail.com
'''

# 检查一个文件是否存在, 如果存在, 就读取它

from __future__ import print_function
import sys		# Import the Modules
import os		# Import the Modules

# 打印用法当且仅当没有被提供的arguments的长度

def usage():
    print('[-] 使用方法: python check_file.py [filename1] [filename2] ... [filenameN]')


# 文件读取
def readfile(filename):
    with open(filename, 'r') as f:      # Ensure file is correctly closed under
        file = f.read()                 # all circumstances
    print(file)
    print()
    print('#'*80)
    print()

def main():
    # Check the arguments passed to the script
    if len(sys.argv) >= 2:
        # print(sys.argv)
        filenames = sys.argv[1:]

        filteredfilenames = list(filenames)
        # Iterate for each filename passed in command line argument
        for filename in filenames:
            if not os.path.isfile(filename):		# Check the File exists
                print('[-] ' + filename + ' does not exist.')
                filteredfilenames.remove(filename)			#remove non existing files from fileNames list
                continue

            # Check you can read the file
            if not os.access(filename, os.R_OK):
                print('[-] ' + filename + ' access denied')
                # remove non readable fileNames
                filteredfilenames.remove(filename)
                continue

        # Read the content of each file that both exists and is readable
        for filename in filteredfilenames:
            # Display Message and read the file contents
            print('[+] Reading from : ' + filename)
            readfile(filename)

    else:
        usage() # Print usage if not all parameters passed/Checked


if __name__ == '__main__':
    main()
