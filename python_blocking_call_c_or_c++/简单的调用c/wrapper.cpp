/*************************************************************************
	> File Name: wrapper.cpp
	> Author: 
	> Mail: 
	> Created Time: 2017年07月13日 星期四 11时38分32秒
 ************************************************************************/
/*
用法：
1. 先转换为xxx.so
    g++ -fPIC wrapper.cpp -o example.so -shared -I /usr/include/python2.7 -I /usr/lib/python2.7/config
2. import ctypes
3. pdll = ctypes.CDLL('/home/afa/myFiles/codeDoc/PythonDoc/python_blocking_call_c_or_c++/简单的调用c/example.so')
4. 调用pdll.fact(4)
*/

#include <Python.h>
#include<iostream>

using namespace std;

class TestFact{
    public:
        TestFact(){};
        ~TestFact(){};
        int fact(int n);
};

int TestFact::fact(int n){
    if(n <= 1)
        return 1;
    else
        return n*(n-1);
}

extern "C"
int fact(int n){
    TestFact t;
    return t.fact(n);
}

