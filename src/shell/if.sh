#[],[[]],(()),test,let

#比较符号：==,!=,-eq,-gt
a=10
b=20
if [ $a == $b ]     #必须要有空格
then
    echo "a等于b"
else
    echo "a不等于b"
fi

if test $a -eq $b
then
    echo "a等于b"
else
    echo "a不等于b"
fi

if [[ $a == $b ]]     #必须要有空格
then
    echo "a等于b"
else
    echo "a不等于b"
fi