from agents import House

'''
Instantiate a House
'''

def orderCreation():
    house = House()
    house.create_order()
    print(house.ordersId)

orderCreation()
