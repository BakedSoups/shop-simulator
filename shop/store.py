# current state 

# all in mem 
# {"items aviable 
# cabinent 1: {capacity} 
# cabinent 2: {capacity}, 
# "}


# carrot juice placed in capacity 
# customer coems in with ask 
# player places carot juice on cabinent 
# farm to table 

# grow carrots in the back
# pick up the carrots 
# juic the carots 


# seats 
# customer profiles
# whats aviable 
# custoemr randomly picks 

# 



# this class will be used for determining what the customer should do 
# seats is a hash 

from dataclasses import dataclass ,field
import random

@dataclass
class CustomerGroup: 
    customer_id: int 
    customer_group_range: int 
    customer_group_count: int = field(init=False)

    def __post_init__(self): 
        self.customer_group_count = random.randint(1, self.customer_group_range) 


class ResturantInfo: 
    def __init__(self, items_available: list[str], seats: list[int], seating_waiting_time: int, outside_waiting_time: int): 
        self.items_available = items_available 
        self.seats = seats 
        self.seating_waiting_time = seating_waiting_time 
        self.outside_waiting_time = outside_waiting_time 


    def seat_customer(self, customer: CustomerGroup): 
        if customer.customer_group_count in self.seats: 




if __name__ == "__main__": 
    items_available = ["grape_juice", "pumkin_juice"]
    # postion is the seat id as well
    # set to a  dictionary  
    
    seats = [4,3,2,4] 

    seating_waiting_time = 10
    outside_waiting_time = 10
    table_max= 2
    
    store_actions = ResturantInfo(items_available, seats, seating_waiting_time,outside_waiting_time)

    customer_1 = CustomerGroup(1, 4) 

    store_actions.seat_customer(customer = customer_1)