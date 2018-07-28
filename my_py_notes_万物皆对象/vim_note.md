# vim 快键键
```bash
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

# 显示行号
:set nu!

### 光标移动操作
# 跳到该行行首
esc+|
# 跳到该行行尾
esc+1+$
# 跳到某行行首(eg:80行首)
:80+|

### 删除操作
# 删除光标所在行
esc+dd
# 多行删除(eg:删除21行到25行)
:21,25d

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

