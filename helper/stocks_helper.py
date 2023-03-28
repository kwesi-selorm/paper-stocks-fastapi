import os


def create_stocks_list():
    stocks_list = []
    file_path = os.path.join(os.path.expanduser("~"), "Downloads", "nasdaq_screener.csv")
    with open(file_path, 'r') as f:
        for line in f:
            line = line.split(",")
            if line[0] == "Symbol":
                continue
            line[2] = line[2].replace("$", "").strip()
            stocks_list.append({"symbol": line[0], "name": line[1], "lastPrice": float(line[2])})
    f.close()

    return stocks_list[90]


print(create_stocks_list())
