import json

read_files = ["data_" + str(x) + ".json" for x in range(700)]
with open("libros.json", "w") as outfile:
    dic = {}
    for f in read_files:
        dic.update( json.loads(open(f, "r",).read()))

    outfile.write(json.dumps(dic))
