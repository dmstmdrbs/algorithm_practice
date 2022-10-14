# find substring(needle) in given string(haystack)
# if not found, return -1
# if found, return index of first occurance position

def strStr(haystack, needle):
    length = len(haystack)
    check_length = len(needle)
    if length < check_length:
        return -1

    for pivot in range(0, length):
        found = True
        for sub_index, char in enumerate(needle):
            if sub_index + pivot >= length:
                return -1
            if char != haystack[sub_index + pivot]:
                found = False
                break
        if found:
            return pivot

    return -1


print(strStr("misssissipissipi",
             "issipi"))
