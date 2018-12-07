#!/usr/bin/pyhton3
#coding=utf-8

f = open('shops.txt')
products = []
price = []

line = f.readline()
while line:
    pro_pri_list = line.split()
    products.append(pro_pri_list[0])
    price.append(pro_pri_list[1])
    line = f.readline()

#print(products, price)
print('欢迎来到SAM商店')
salary = int(input("请输入你的充值金额: "))
print('你可以购买如下商品:')

p_index_l = []
for p in products:
    p_index = products.index(p)
    p_index_l.append(p_index)
    p_price = price[p_index]
    print("商品序号:%s  商品名称:%s  商品价格:%s" % (p_index, p, p_price))

#print(p_index_l)
while True:
    c_index = int(input("请输入你要购买商品的序号:").strip())
    c_price = int(price[c_index])
    print("商品价格为:%s " % c_price)
    if c_index in p_index_l and salary >= c_price:
        print("购买成功!")
        salary = salary - c_price
        print("你当前的余额为:", salary)
        
        while True:
            choice = input("你是继续购买(b)还是退出(q): ")
            if choice == "b":
                choice = 1
                break
            elif choice == "q":
                choice = 0
                break
            else: 
                print("请做出正确选择!")
        if choice:
            continue
        else:
            break 

    else:
        print("请确认你选择的商品是否存在? 或者你的余额足够支付?")

