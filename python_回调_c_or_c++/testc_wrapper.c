/*************************************************************************
	> File Name: testc_wrapper.c
	> Author: 
	> Mail: 
	> Created Time: 2017年07月02日 星期日 08时18分06秒
 ************************************************************************/

#include "Python.h"  //包含python头文件
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include "testC.h"

//包名+函数名
static PyObject *test_fac(PyObject *self, PyObject *args){
    int num;
    //把从python中用户传递的args以i的形式转换并赋值给c中的int类型的num
    if(!PyArg_ParseTuple(args, "i", &num))
        return NULL;
    //把c的类型转换为python所识别的类型int,结果为python类型的int
    return (PyObject *)Py_BuildValue("i", fac(num));
}

static PyObject *test_doppel(PyObject *self, PyObject *args){
    char *src;
    char *mstr;
    PyObject *retval;
    //把python中的str类型以s的形式转换成c中的char *类型
    //如果转换不成功则返回null
    if(!PyArg_ParseTuple(args, "s", &src))
        return NULL;

    mstr = malloc(strlen(src) + 1);
    strcpy(mstr, src);
    reverse(mstr);
    retval = (PyObject *)Py_BuildValue("ss", src, mstr);
    free(mstr);

    return retval;
}

static PyObject *test_test(PyObject *self, PyObject *args){
    test();
    return (PyObject *)Py_BuildValue("");
}

static PyMethodDef testMethods[] = {
    //c函数名 包裹函数名 METH_VARARGS
    {"fac", test_fac, METH_VARARGS},
    {"doppel", test_doppel, METH_VARARGS},
    {"test", test_test, METH_VARARGS},
    {NULL, NULL},
};

//初始化函数
void inittest(void){
    Py_InitModule("test", testMethods);
}


