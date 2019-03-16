data = [{"name": "cat1", "children":[{"name":"cat11", "children": [{"name": "cat111", "children":[
 {"name":"cat1111"}, {"name":"cat1112"},{"name":"cat1113"}]},
 {"name":"cat112", "children":[{"name":"cat1121"}, {"name":"cat1122"}, {"name":"cat1123"}]}]},
                                 {"name":"cat12", "children":[{"name":"cat121"}, {"name":"cat122", "children":[
                                  {"name":"cat1221"}, {"name":"cat1222"}]}]}]}]
d = {}
while data:
    new_data=[]
    for item in data:
        print(item)
        if item['name'] not in d.keys():
            d[item['name']] = []

        if 'children' in item:
            for child in item['children']:
                if child['name'] not in d.keys():
                    d[child['name']] = []
                d[item['name']].append(child['name'])

                new_data.append(child)

    data = new_data

print(d)