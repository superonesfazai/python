# vim 快键键
```bash
### 命令补全
tab

### 菜单操作
# 打开菜单
:NERDTree

### 多窗口操作
# 左右垂直新开窗口
:vsp path
# 上下水平新开窗口
:sp path
# 多窗口上下切换
:ctrl+w+j/k

### 行号
# 显示行号
:set nu
# 取消行号
:set nonu

### 光标移动操作
# 跳到该行行首
esc+|
# 跳到该行行尾
esc+1+$
# 跳到某行行首(eg:80行首)
:80+|
# 跳到文件最后一行
:$
# 跳到文件最开头
:0

### 粘贴
# 光标下一行粘贴
esc+p
# 光标上一行粘贴
esc+P

### 删除操作
# 删除光标所在行
esc+dd
# 多行删除(eg:删除21行到25行)
:21,25d

### 插入行
# 当前行下方插入一行
esc+o

### 搜索
# 光标下方搜索
esc+/
# 光标上方搜索
esc+?

### 撤销操作
esc+u

### 执行python3(当前.py文件)
:!python %
# F5一键编译
$ vi ~/.vimrc
# 加入下面代码
map <F5> :call CompileRunGcc()<CR>

func! CompileRunGcc()
    exec "w" 
    if &filetype == 'c' 
        exec '!g++ % -o %<'
        exec '!time ./%<'
    elseif &filetype == 'cpp'
        exec '!g++ % -o %<'
        exec '!time ./%<'
    elseif &filetype == 'python'
        exec '!time python3 %'
    elseif &filetype == 'sh'
        :!time bash %
    endif                                                                              
endfunc
```

