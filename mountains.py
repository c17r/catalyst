from datetime import datetime

now = datetime.now()
print now.strftime("%Y-%m-%d %H:%M:%S (%A)")
print ""

lines = [l.rstrip() for l in open("mountains-1.csv", "r")]
del lines[0]
for line in lines:
    data = line.split(",")
    data[5] = "unknown" if data[5] == "null" else data[5]
    print "%s has an altitude of %s meters." % (data[1], data[5])
