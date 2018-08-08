scp对拷文件和文件夹下的所有文件对拷文件并重命名

1. 对拷文件夹(包括文件夹本身)
```bash
scp -r /home/wwwroot/www/charts/util root@192.168.1.65:/home/wwwroot/limesurvey_back/scp
```
2. 对拷文件夹下的所有文件(不包括文件本身)
```bash
scp /home/wwwroot/www/charts/util/* root@192.168.1.65:/home/wwwroot/limesurvey_back/scp
```
3. 对拷文件并重命名
```bash
scp /home/wwwroot/www/charts/utils/* root@192.168.1.65:/home/wwwroot/limesurvey_back/scp/b.text
```