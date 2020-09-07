import json

js = json.load(open('temp.json', 'r'))

# print(js["k=4_n=60_p=0.1"]["settings"])

s = ""
for case in js:
    values = js[case]['statistics']
    i = 0
    for v in values:
        if i < 5:
            i+=1
            continue
        s += "{0:.1f} & ".format(values[v]['best_cost'])
        s += "{0:.1f} & ".format(values[v]['mean'])
    s += "\\\\ \n"
# print(s)
out = open('out.txt', 'w')
out.write(s)