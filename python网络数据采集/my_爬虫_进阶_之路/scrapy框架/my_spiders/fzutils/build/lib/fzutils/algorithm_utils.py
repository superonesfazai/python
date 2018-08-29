# coding:utf-8

"""
算法utils
"""

from random import shuffle

__all__ = [
    'bubble_sort',                          # 冒泡排序法
    'insertion_sort',                       # 插入排序法
    'selection_sort',                       # 选择排序法
    'quick_sort',                           # 快速排序法
    'bogo_sort',                            # 猴子排序法
    'merge_sort',                           # 归并排序法
    'shell_sort',                           # 希尔排序法
    'heap_sort',                            # 堆排序法
    'cocktail_shaker_sort',                 # 鸡尾酒排序法(即:定向冒泡排序法)
]

def bubble_sort(collection):
    '''
    冒泡排序法
    :param collection: 只支持list
    :return:
    '''
    length = len(collection)
    for i in range(length-1, -1, -1):
        for j in range(i):
            if collection[j] > collection[j+1]:
                collection[j], collection[j+1] = collection[j+1], collection[j]

    return collection

def insertion_sort(collection):
    '''
    插入排序法
    :param collection: list
    :return:
    '''
    for index in range(1, len(collection)):
        while 0 < index and collection[index] < collection[index - 1]:
            collection[index], collection[
                index - 1] = collection[index - 1], collection[index]
            index -= 1

    return collection

def selection_sort(collection):
    '''
    选择排序法
    :param collection: list
    :return:
    '''
    length = len(collection)
    for i in range(length):
        least = i
        for k in range(i + 1, length):
            if collection[k] < collection[least]:
                least = k
        collection[least], collection[i] = (
            collection[i], collection[least]
        )

    return collection

def quick_sort(collection):
    '''
    快速排序法
    :param collection: list
    :return:
    '''
    ARRAY_LENGTH = len(collection)
    if( ARRAY_LENGTH <= 1):
        return collection
    else:
        PIVOT = collection[0]
        GREATER = [ element for element in collection[1:] if element > PIVOT ]
        LESSER = [ element for element in collection[1:] if element <= PIVOT ]

        return quick_sort(LESSER) + [PIVOT] + quick_sort(GREATER)

def bogo_sort(collection):
    '''
    猴子排序法
    :param collection: list
    :return:
    '''
    def isSorted(collection):
        if len(collection) < 2:
            return True
        for i in range(len(collection) - 1):
            if collection[i] > collection[i + 1]:
                return False
        return True

    while not isSorted(collection):
        shuffle(collection)

    return collection

def merge_sort(collection):
    '''
    归并排序法
    :param collection: list
    :return:
    '''
    length = len(collection)
    if length > 1:
        midpoint = length // 2
        left_half = merge_sort(collection[:midpoint])
        right_half = merge_sort(collection[midpoint:])
        i = 0
        j = 0
        k = 0
        left_length = len(left_half)
        right_length = len(right_half)
        while i < left_length and j < right_length:
            if left_half[i] < right_half[j]:
                collection[k] = left_half[i]
                i += 1
            else:
                collection[k] = right_half[j]
                j += 1
            k += 1

        while i < left_length:
            collection[k] = left_half[i]
            i += 1
            k += 1

        while j < right_length:
            collection[k] = right_half[j]
            j += 1
            k += 1

    return collection

def shell_sort(collection):
    '''
    希尔排序法
    :param collection: list
    :return:
    '''
    # Marcin Ciura's gap sequence
    gaps = [701, 301, 132, 57, 23, 10, 4, 1]

    for gap in gaps:
        i = gap
        while i < len(collection):
            temp = collection[i]
            j = i
            while j >= gap and collection[j - gap] > temp:
                collection[j] = collection[j - gap]
                j -= gap
            collection[j] = temp
            i += 1

    return collection

def heap_sort(collection):
    '''
    堆排序法
    :param collection:
    :return:
    '''
    def heapify(unsorted, index, heap_size):
        largest = index
        left_index = 2 * index + 1
        right_index = 2 * index + 2
        if left_index < heap_size and unsorted[left_index] > unsorted[largest]:
            largest = left_index

        if right_index < heap_size and unsorted[right_index] > unsorted[largest]:
            largest = right_index

        if largest != index:
            unsorted[largest], unsorted[index] = unsorted[index], unsorted[largest]
            heapify(unsorted, largest, heap_size)

    n = len(collection)
    for i in range(n // 2 - 1, -1, -1):
        heapify(collection, i, n)
    for i in range(n - 1, 0, -1):
        collection[0], collection[i] = collection[i], collection[0]
        heapify(collection, 0, i)

    return collection

def cocktail_shaker_sort(collection):
    '''
    鸡尾酒排序法(即:定向冒泡排序法)
    :param collection:
    :return:
    '''
    for i in range(len(collection) - 1, 0, -1):
        swapped = False

        for j in range(i, 0, -1):
            if collection[j] < collection[j - 1]:
                collection[j], collection[j - 1] = collection[j - 1], collection[j]
                swapped = True

        for j in range(i):
            if collection[j] > collection[j + 1]:
                collection[j], collection[j + 1] = collection[j + 1], collection[j]
                swapped = True

        if not swapped:
            return collection
