from collections import Counter, deque


def sort_array(arr):
    counter = Counter(arr)
    set_arr = list(set(arr))
    # set_arr.sort(key=lambda x: counter[x])

    new_arr = []
    for num in set_arr:
        if num == 0:
            continue
        new_arr.append((num, counter[num]))

    new_arr.sort(key=lambda x: (x[1], x[0]))
    new_counter_list = []
    for num, count in new_arr:
        new_counter_list.append(num)
        new_counter_list.append(count)

    return new_counter_list


def calculate(arr, op):
    if op == 'C':
        arr = list(map(list, zip(*arr)))

    row_len = len(arr)

    max_row_len = -1
    new_arr = []
    for i in range(row_len):
        new_row = sort_array(arr[i])
        new_arr.append(new_row)
        new_length = len(new_row)

        if new_length > max_row_len:
            max_row_len = new_length

    if max_row_len > 100:
        max_row_len = 100

    for i in range(row_len):
        new_arr[i].extend([0]*max_row_len)
        new_arr[i] = new_arr[i][:max_row_len]

    new_arr = new_arr if op == 'R' else list(map(list, zip(*new_arr)))
    return new_arr


def print_arr(arr):
    for row in arr:
        print(row)
    print()


def get_time():
    r, c, k = map(int, input().split(' '))
    r = r-1
    c = c-1
    A = [list(map(int, input().split(' '))) for _ in range(3)]
    # print_arr(A)

    for i in range(0, 101):
        row_len = len(A)
        col_len = len(A[0])
        # print_arr(A)
        # print('time', i)
        # print_arr(A)
        if 0 <= r < row_len and 0 <= c < col_len and A[r][c] == k:
            # print('r,c,k,A[r][c]', r, c, k, A[r][c])
            return i

        op = 'R'
        if row_len >= col_len:
            op = 'R'
        else:
            op = 'C'

        A = calculate(A, op)
    return -1


print(get_time())
