#>输出重定向
#echo "123">aaa.txt

#1标准输出,系统默认为1
#echo "111" 1>aaa.txt
#echo "111">aaa.txt

#2标准错误输出
#ls sssssssssss

#重定向2>&1，原来作为错误输出，现在指定到1的输出,1可以省略
#ls sssssssssss 1>aaa.txt 2>&1

#标准输出，标准输出到控设备文件，也就是不输出
echo "test" 1>/dev/null