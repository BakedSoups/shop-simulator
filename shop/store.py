from dataclasses import dataclass, field
import random


@dataclass
class CustomerInfo:
    id: int
    order: list
    indoor_seating_time: int
    outdoor_seating_time: int


@dataclass
class CustomerGroup:
    id: int
    group_range: int
    group_count: int = field(init=False)

    def __post_init__(self):
        self.group_count = random.randint(1, self.group_range)


@dataclass
class Table:
    id: int
    size: int
    taken: bool = False
    customers: list[CustomerInfo] = field(default_factory=list)


class Resturant:
    def __init__(self, items_available: list, tables: list[Table]):
        self.items_available = items_available
        self.tables = tables
        self.next_customer_id = 1

    def seat_customer(self, customer_group: CustomerGroup):
        for table in self.tables:
            if not table.taken and table.size >= customer_group.group_count:
                table.taken = True

                for _ in range(customer_group.group_count):
                    customer = CustomerInfo(
                        id=self.next_customer_id,
                        order=[random.choice(self.items_available)],
                        indoor_seating_time=5,
                        outdoor_seating_time=5
                    )

                    self.next_customer_id += 1
                    table.customers.append(customer)

                return table.id

        return None

    def customer_order(self):
        return random.choice(self.items_available)


if __name__ == "__main__":
    items_available = ["grape_juice", "pumkin_juice"]

    tables = [
        Table(id=1, size=5),
        Table(id=2, size=2)
    ]

    store_actions = Resturant(items_available, tables)

    customer_1 = CustomerGroup(id=1, group_range=4)

    seated_table_id = store_actions.seat_customer(customer_1)

    print("Seated at table:", seated_table_id)
    print(store_actions.tables)