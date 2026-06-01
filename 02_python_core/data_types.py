def data_types():
    list_e = [1, '2', 3.3, True, [1, 2, 3, 'apple', 'banana'], dict(Alice=24, Bob=30, Karl=27), (1,2,3,4,5), set("aaassdf")]
    print("[", end="")
    for x in range(len(list_e)):
        if x != len(list_e)-1:
            print(str(type(list_e[x])).split("'")[1], end=", ")
        else:
            print(str(type(list_e[x])).split("'")[1], end="")
    print("]")
if __name__ == '__main__':
    data_types()