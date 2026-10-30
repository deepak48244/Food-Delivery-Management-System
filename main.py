"""Food Delivery Management System - Console Edition (Python OOP + DSA)."""
import csv
import os
from abc import ABC, abstractmethod
from collections import deque
from datetime import datetime

BASE = os.path.dirname(os.path.abspath(__file__))
ORDER_FIELDS = ['order_id', 'customer', 'phone', 'items', 'total', 'status', 'date']


def read_csv(filename):
    with open(os.path.join(BASE, filename), newline='', encoding='utf-8') as file:
        return list(csv.DictReader(file))


def write_csv(filename, fields, rows):
    with open(os.path.join(BASE, filename), 'w', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


class Person(ABC):
    def __init__(self, name, phone):
        self.name = name
        self.__phone = phone  # encapsulation

    @property
    def phone(self):
        return self.__phone

    @abstractmethod
    def details(self):
        pass


class Customer(Person):
    def details(self):  # polymorphism / method implementation
        return f'{self.name} ({self.phone})'


class Restaurant:
    def __init__(self, data):
        self.id = data['restaurant_id']
        self.name = data['name']
        self.location = data['location']

    def details(self):
        return f'{self.id}. {self.name} - {self.location}'


class FoodItem:
    def __init__(self, data):
        self.id = data['food_id']
        self.name = data['name']
        self.price = int(data['price'])
        self.restaurant_id = data['restaurant_id']
        self.category = data['category']


class CartStack:
    """Stack: push to add food; pop to undo last addition (LIFO)."""
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop() if self.items else None

    def total(self):
        return sum(item.price for item in self.items)

    def clear(self):
        self.items.clear()


class OrderQueue:
    """Queue: pending orders processed first-in-first-out (FIFO)."""
    def __init__(self, orders):
        self.queue = deque(o['order_id'] for o in orders if o['status'] == 'Pending')

    def enqueue(self, order_id):
        self.queue.append(order_id)

    def dequeue(self):
        return self.queue.popleft() if self.queue else None


def linear_search(items, keyword):
    """Linear search: O(n)."""
    keyword = keyword.casefold()
    return [item for item in items if keyword in item.name.casefold()]


def merge_sort(items):
    """Sort by price using merge sort: O(n log n)."""
    if len(items) <= 1:
        return items[:]
    mid = len(items) // 2
    left, right = merge_sort(items[:mid]), merge_sort(items[mid:])
    result = []
    i = j = 0
    while i < len(left) and j < len(right):
        if left[i].price <= right[j].price:
            result.append(left[i]); i += 1
        else:
            result.append(right[j]); j += 1
    return result + left[i:] + right[j:]


class FoodDeliverySystem:
    def __init__(self):
        self.restaurants = [Restaurant(row) for row in read_csv('restaurants.csv')]
        self.food = [FoodItem(row) for row in read_csv('food_items.csv')]
        self.food_by_id = {item.id: item for item in self.food}  # hash map, avg O(1)
        self.restaurant_by_id = {r.id: r for r in self.restaurants}
        self.orders = read_csv('orders.csv')
        self.queue = OrderQueue(self.orders)
        self.cart = CartStack()

    def show_food(self, items):
        if not items:
            print('No matching food items found.')
            return
        print(f"{'ID':<7}{'Food Name':<28}{'Price':<10}Restaurant")
        print('-' * 75)
        for item in items:
            restaurant = self.restaurant_by_id.get(item.restaurant_id)
            print(f'{item.id:<7}{item.name[:27]:<28}Rs.{item.price:<7}{restaurant.name if restaurant else "Unknown"}')

    def show_restaurants(self):
        for restaurant in self.restaurants:
            print(restaurant.details())
        rid = input('Enter restaurant ID for its menu (or Enter to go back): ').strip()
        if rid:
            if rid not in self.restaurant_by_id:
                print('Invalid restaurant ID.')
            else:
                self.show_food([item for item in self.food if item.restaurant_id == rid])

    def add_to_cart(self):
        fid = input('Enter Food ID: ').strip()
        item = self.food_by_id.get(fid)
        if item is None:
            print('Food ID not found.')
            return
        try:
            qty = int(input('Quantity (1-20): '))
            if not 1 <= qty <= 20:
                raise ValueError
        except ValueError:
            print('Enter a valid quantity between 1 and 20.')
            return
        for _ in range(qty):
            self.cart.push(item)
        print(f'Added {qty} x {item.name} to cart.')

    def show_cart(self):
        if not self.cart.items:
            print('Cart is empty.')
            return
        self.show_food(self.cart.items)
        print(f'Total: Rs.{self.cart.total()}')

    def checkout(self):
        if not self.cart.items:
            print('Cart is empty. Add food first.')
            return
        name = input('Customer name: ').strip()
        phone = input('Phone number (10 digits): ').strip()
        if not name or not (phone.isdigit() and len(phone) == 10):
            print('Please enter a name and a valid 10-digit phone number.')
            return
        customer = Customer(name, phone)
        print('Customer:', customer.details())
        self.show_cart()
        if input('Confirm order? (y/n): ').strip().lower() != 'y':
            print('Checkout cancelled.')
            return
        next_id = max((int(o['order_id']) for o in self.orders if o['order_id'].isdigit()), default=1000) + 1
        row = {
            'order_id': str(next_id), 'customer': customer.name, 'phone': customer.phone,
            'items': '; '.join(item.id for item in self.cart.items),
            'total': str(self.cart.total()), 'status': 'Pending',
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        self.orders.append(row)
        write_csv('orders.csv', ORDER_FIELDS, self.orders)
        customers = read_csv('customers.csv')
        if not any(c['phone'] == phone for c in customers):
            customers.append({'name': name, 'phone': phone})
            write_csv('customers.csv', ['name', 'phone'], customers)
        self.queue.enqueue(row['order_id'])
        self.cart.clear()
        print(f'Order placed successfully! Order ID: {next_id} | Total: Rs.{row["total"]}')

    def show_orders(self):
        if not self.orders:
            print('No orders placed yet.')
            return
        print(f"{'Order ID':<12}{'Customer':<20}{'Total':<12}{'Status':<14}Date")
        print('-' * 80)
        for order in self.orders:
            print(f"{order['order_id']:<12}{order['customer'][:19]:<20}Rs.{order['total']:<9}{order['status']:<14}{order['date']}")

    def track_order(self):
        oid = input('Enter Order ID: ').strip()
        order = next((o for o in self.orders if o['order_id'] == oid), None)
        if not order:
            print('Order not found.')
            return
        print(f"Order #{oid} | Customer: {order['customer']} | Status: {order['status']} | Total: Rs.{order['total']}")

    def process_next_order(self):
        oid = self.queue.dequeue()
        if oid is None:
            print('No pending orders in queue.')
            return
        order = next(o for o in self.orders if o['order_id'] == oid)
        order['status'] = 'Delivered'
        write_csv('orders.csv', ORDER_FIELDS, self.orders)
        print(f'Order #{oid} processed (FIFO) and marked Delivered.')

    def run(self):
        actions = {
            '1': self.show_restaurants,
            '2': lambda: self.show_food(self.food),
            '3': lambda: self.show_food(linear_search(self.food, input('Search food name: ').strip())),
            '4': lambda: self.show_food(merge_sort(self.food)),
            '5': self.add_to_cart,
            '6': self.show_cart,
            '7': self.undo_last,
            '8': self.checkout,
            '9': self.show_orders,
            '10': self.track_order,
            '11': self.process_next_order,
        }
        while True:
            print('\n' + '=' * 52)
            print(' FOOD DELIVERY MANAGEMENT SYSTEM')
            print(' Name       : Deepak Kumar')
            print(' Reg No.    : 251302172')
            print(' Course     : BTech CSE (AI&ML)')
            print(' Section    : 3C')
            print('=' * 52)
            print('1. View Restaurants       2. View All Food')
            print('3. Search Food            4. Sort by Price (Merge Sort)')
            print('5. Add to Cart            6. View Cart')
            print('7. Undo Last Cart Item    8. Place Order')
            print('9. Order History         10. Track Order')
            print('11. Process Next Order   12. Exit')
            choice = input('Enter choice: ').strip()
            if choice == '12':
                print('Thank you for using Food Delivery Management System!')
                break
            action = actions.get(choice)
            if action:
                action()
            else:
                print('Invalid choice. Please try again.')

    def undo_last(self):
        item = self.cart.pop()
        print(f'Removed {item.name} (Stack LIFO).' if item else 'Cart is empty.')


if __name__ == '__main__':
    try:
        FoodDeliverySystem().run()
    except (FileNotFoundError, KeyError, ValueError) as exc:
        print('Dataset error:', exc)
        print('Keep all CSV files in the same folder as main.py.')
