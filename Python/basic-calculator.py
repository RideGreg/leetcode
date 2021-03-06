# Time:  O(n)
# Space: O(n)
# 224
# Implement a basic calculator to evaluate a simple expression string.
#
# The expression string may contain open ( and closing parentheses ),
# the plus + or minus sign -, non-negative integers and empty spaces .
#
# You may assume that the given expression is always valid.
#
# Some examples:
# "1 + 1" = 2
# " 2-1 + 2 " = 3
# "(1+(4+5+2)-3)+(6+8)" = 23
#

try:
    xrange          # Python 2
except NameError:
    xrange = range  # Python 3

# Why stack?
# No matter left to right or right to left, need to get previous operand, so stack is perfect.

# Why backward scan?
# If forward scan the input, we end up calculate from right to left, not easy to handle subtraction '(A-B)-C'.
# so we scan from right to left, and calculate starting from left.

import operator


class Solution(object):
    def calculate(self, s):  # prefer not to use, fancy/general but not simple code
        """
        :type s: str
        :rtype: int
        """
        def compute(operands, operators):
            right, left = operands.pop(), operands.pop()
            operands.append(ops[operators.pop()](left, right))

        ops = {'+':operator.add, '-':operator.sub, '*':operator.mul, '/':operator.div}
        precedence = {'+':0, '-':0, '*':1, '/':1}
        operands, operators, operand = [], [], 0
        for i in xrange(len(s)):
            if s[i].isdigit():
                operand = operand*10 + int(s[i])
                if i == len(s)-1 or not s[i+1].isdigit():
                    operands.append(operand)
                    operand = 0
            elif s[i] == '(':
                operators.append(s[i])
            elif s[i] == ')':
                while operators[-1] != '(':
                    compute(operands, operators)
                operators.pop()
            elif s[i] in precedence:
                while operators and operators[-1] in precedence and \
                      precedence[operators[-1]] >= precedence[s[i]]:
                    compute(operands, operators)
                operators.append(s[i])
        while operators:
            compute(operands, operators)
        return operands[-1]


# Time:  O(n)
# Space: O(n)

# Edge case: starting with '-'
class Solution2(object):
    # @param {string} s
    # @return {integer}
    def calculate(self, s):  # USE THIS
        operands, operators = [], []
        if s.lstrip()[0] == '-': s = '0'+s
        s = '#'+s

        curNum = ''
        for c in reversed(s):
            if c.isdigit():
                curNum += c    # if forward scan, can use curNum = curNum*10 + int(c)
            else:
                # non digit, first push the complete num to stack
                if curNum != '':
                    operands.append(int(curNum[::-1]))
                    curNum = ''

                if c in ')+-':
                    operators.append(c)
                elif c == '(':
                    while operators[-1] != ')':
                        self.compress(operands, operators)
                    operators.pop()

        while operators:
            self.compress(operands, operators)

        return operands[-1]


    def calculate_kamyu(self, s):
        if s.lstrip()[0] == '-':     # edge case: start with '-'
            s = '0' + s

        operands, operators = [], [] # use 1 stack doesn't work '(3+1)', because ) was stored in bottom.
                                     # Need to pop ')' before storing the sum.
        operand = ""
        for i in reversed(xrange(len(s))):
            if s[i].isdigit():
                operand += s[i]
                if i == 0 or not s[i-1].isdigit():  # this is bad checking every time. Should do only once after number is finished.
                    operands.append(int(operand[::-1]))
                    operand = ""
            elif s[i] in ')+-':
                operators.append(s[i])
            elif s[i] == '(':
                while operators[-1] != ')':
                    self.compress(operands, operators)
                operators.pop()         # pop out ')'
            #else: skip for empty space ' '

        while operators:
            self.compress(operands, operators)

        return operands[-1]


    def compress(self, operands, operators):
        left, right = operands.pop(), operands.pop()
        op = operators.pop()
        operands.append(left + right if op == '+' else left - right)


print(Solution().calculate("7 + 1")) # 8
print(Solution().calculate("3-1 + 2")) # 4
print(Solution().calculate("(1+(4+5+2)-3)+(6+8)")) # 23
print(Solution().calculate("- 1")) # -1
print(Solution().calculate("-(1 + 2)")) # -3


