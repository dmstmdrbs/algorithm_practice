
import re


def isPalindrome(s):
    """
    :type s: str
    :rtype: bool
    """

    string = re.sub('[^a-zA-Z0-9]', '', s)
    string = string.lower()
    left = 0
    right = len(string)-1
    while left < right:
        left_char = string[left]
        right_char = string[right]
        if left_char != right_char:
            return False

        left += 1
        right -= 1
    return True
