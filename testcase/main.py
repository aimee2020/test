import os
import sys
import time


def get_all_dir(cwd):
    get_dir = os.listdir(cwd)

    result = []
    for i in get_dir:

        sub_dir = os.path.join(cwd, i)
        if os.path.isdir(sub_dir):
            result.append(i)
            print(i)

    return result


if __name__ == '__main__':
    res = get_all_dir(os.getcwd())
    print(res)
    for i in res:
        if i != 'interface' and i != 'inter':
            # os.system('cd ./'+i)
            print('-----------------------------' + i + ' start -----------------------------')
            os.chdir(sys.path[0] + '\\' + i)
            # for num in range(1, 1):
            os.system('python Interface.py')
            # num = num + 1
            print('-----------------------------' + i + ' end -----------------------------')

    # print(os.getcwd())
    print(__file__, sys.path[0])
    print(time.strftime("%Y-%m-%d", time.localtime(time.time())))
