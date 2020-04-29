# tmux
list sessions
```bash
$ tmux ls
11: 1 windows (created Tue Aug 27 14:58:12 2019)
12: 1 windows (created Sat Sep  7 09:49:04 2019)
14: 1 windows (created Sat Sep  7 09:50:23 2019)
tm0: 1 windows (created Sat Sep  7 09:49:17 2019)
```
kill session:
```bash
$ tmux kill-session -t 11[myname]
```
start new with session name:
```bash
$ tmux new -s myname
```
attach
```bash
$ tmux attach -t myname
```
关闭所有会话
```bash
$ tmux ls | grep : | cut -d. -f1 | awk '{print substr($1, 0, length($1)-1)}' | xargs kill
```