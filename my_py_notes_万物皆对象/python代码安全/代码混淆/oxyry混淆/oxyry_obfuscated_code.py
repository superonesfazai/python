# coding:utf-8

'''
@author = super_fazai
@File    : oxyry_obfuscated_code.py
@connect : superonesfazai@gmail.com
'''

"""
基于http://pyob.oxyry.com/的代码混淆工具
"""

from os import walk
from fzutils.ip_pools import tri_ip_pool
from fzutils.spider.async_always import *

# TEST
# TARGET_FOLDER_PATH = '/Users/afa/myFiles/codeDoc/pythonDoc/python/my_py_notes_万物皆对象/python代码安全/代码混淆/oxyry混淆/test'
TARGET_FOLDER_PATH = '/Users/afa/Desktop/always/伪装cp_code/my_flask_server'

class OXYRYObfuscatedCoder(AsyncCrawler):
    def __init__(self, *params, **kwargs):
        AsyncCrawler.__init__(
            self,
            *params,
            **kwargs,
            ip_pool_type=tri_ip_pool,)

    async def _fck_run(self):
        """
        main
        :return:
        """
        tasks = []
        for item in walk(TARGET_FOLDER_PATH):
            # item 返回的是一个三元tupple(dirpath, dirnames, filenames)
            # print(item)
            dir_path, dir_names, file_names = item
            for file_name in file_names:
                # print('file_name: {}'.format(file_name))
                if re.compile('\.py').findall(file_name) == [] \
                        or re.compile('\.pyc').findall(file_name) != []:
                    # 跳过非py文件
                    continue

                target_code_str = ''
                # encoding='latin1' 处理python3 UnicodeDecodeError: 'ascii' codec can't decode byte
                with open(dir_path + '/' + file_name, 'r', encoding='latin1') as f:
                    # target_code_str = f.read().decode('utf-8').replace('    ', '\t')
                    for line in f:
                        target_code_str += line.replace('    ', '\t')
                # print(r'{}'.format(target_code_str))

                print('create task[where file_name: {}/{}]...'.format(dir_path, file_name))
                tasks.append(self.loop.create_task(self._get_obfuscated_api_res(
                    dir_path=dir_path,
                    file_name=file_name,
                    target_code_str=target_code_str,)))
                
        all_res = await async_wait_tasks_finished(tasks=tasks)
        for i in all_res:
            dir_path, file_name, obfuscated_res = i
            with open(dir_path + '/' + file_name, 'w', encoding='latin1') as f:
                f.write(obfuscated_res)
        
        print('all finished!')

    async def _get_obfuscated_api_res(self, dir_path, file_name, target_code_str:str) -> tuple:
        """
        获取混淆代码接口的结果
        :return:
        """
        headers = get_base_headers()
        headers.update({
            'Origin': 'http://pyob.oxyry.com',
            'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8',
            'content-type': 'application/json',
            'Referer': 'http://pyob.oxyry.com/',
            'Connection': 'keep-alive',
        })
        url = 'http://pyob.oxyry.com/obfuscate'
        # 此处得转成json来传递
        data = dumps({
            'append_source': False,
            'preserve': '',
            'remove_docstrings': True,              # 删除注释
            'rename_default_parameters': True,
            'rename_nondefault_parameters': True,
            'source': target_code_str,              # 待转换源码
        })
        # data = '{"append_source":false,"remove_docstrings":true,"rename_nondefault_parameters":true,"rename_default_parameters":false,"preserve":"","source":"\\"\\"\\"The n queens puzzle.\\n\\nhttps://github.com/sol-prog/N-Queens-Puzzle/blob/master/nqueens.py\\n\\"\\"\\"\\n\\n__all__ = []\\n\\nclass NQueens:\\n    \\"\\"\\"Generate all valid solutions for the n queens puzzle\\"\\"\\"\\n    \\n    def __init__(self, size):\\n        # Store the puzzle (problem) size and the number of valid solutions\\n        self.__size = size\\n        self.__solutions = 0\\n        self.__solve()\\n\\n    def __solve(self):\\n        \\"\\"\\"Solve the n queens puzzle and print the number of solutions\\"\\"\\"\\n        positions = [-1] * self.__size\\n        self.__put_queen(positions, 0)\\n        print(\\"Found\\", self.__solutions, \\"solutions.\\")\\n\\n    def __put_queen(self, positions, target_row):\\n        \\"\\"\\"\\n        Try to place a queen on target_row by checking all N possible cases.\\n        If a valid place is found the function calls itself trying to place a queen\\n        on the next row until all N queens are placed on the NxN board.\\n        \\"\\"\\"\\n        # Base (stop) case - all N rows are occupied\\n        if target_row == self.__size:\\n            self.__show_full_board(positions)\\n            self.__solutions += 1\\n        else:\\n            # For all N columns positions try to place a queen\\n            for column in range(self.__size):\\n                # Reject all invalid positions\\n                if self.__check_place(positions, target_row, column):\\n                    positions[target_row] = column\\n                    self.__put_queen(positions, target_row + 1)\\n\\n\\n    def __check_place(self, positions, ocuppied_rows, column):\\n        \\"\\"\\"\\n        Check if a given position is under attack from any of\\n        the previously placed queens (check column and diagonal positions)\\n        \\"\\"\\"\\n        for i in range(ocuppied_rows):\\n            if positions[i] == column or \\\\\\n                positions[i] - i == column - ocuppied_rows or \\\\\\n                positions[i] + i == column + ocuppied_rows:\\n\\n                return False\\n        return True\\n\\n    def __show_full_board(self, positions):\\n        \\"\\"\\"Show the full NxN board\\"\\"\\"\\n        for row in range(self.__size):\\n            line = \\"\\"\\n            for column in range(self.__size):\\n                if positions[row] == column:\\n                    line += \\"Q \\"\\n                else:\\n                    line += \\". \\"\\n            print(line)\\n        print(\\"\\\\n\\")\\n\\n    def __show_short_board(self, positions):\\n        \\"\\"\\"\\n        Show the queens positions on the board in compressed form,\\n        each number represent the occupied column position in the corresponding row.\\n        \\"\\"\\"\\n        line = \\"\\"\\n        for i in range(self.__size):\\n            line += str(positions[i]) + \\" \\"\\n        print(line)\\n\\ndef main():\\n    \\"\\"\\"Initialize and solve the n queens puzzle\\"\\"\\"\\n    NQueens(8)\\n\\nif __name__ == \\"__main__\\":\\n    # execute only if run as a script\\n    main()\\n"}'
        body = await unblock_request(
            method='post',
            url=url,
            headers=headers,
            data=data,
            ip_pool_type=self.ip_pool_type,
            num_retries=35,)
        # print(body)
        data = json_2_dict(
            json_str=body,
            default_res={}).get('dest', '').replace('    ', '\t')
        # print(data)
        print('[{}] file_name: {}/{}'.format(
            '+' if data != '' else '-',
            dir_path,
            file_name))

        return (dir_path, file_name, data)

if __name__ == '__main__':
    _ = OXYRYObfuscatedCoder()
    loop = get_event_loop()
    res = loop.run_until_complete(_._fck_run())