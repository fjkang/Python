inputs = raw_input()
print inputs
string = inputs.replace(' ', '')
print string
result = {}
i = 0
while i < len(string)-1:
    if string[i] in result.keys():
        result[string[i]] += 1
    else:
        result[string[i]] = 1
    i += 1
print result
for k in result:
    print k, ':', result[k]
