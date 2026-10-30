# Food Delivery Management System — Console Version

**Student:** Deepak Kumar  
**Registration:** 251302172  
**Program:** BTech CSE (AI&ML), Section 3C

## Run

1. Install Python 3.
2. Extract the ZIP, keeping all CSV files with `main.py`.
3. Open a terminal in the project folder.
4. Run `python main.py` (Windows) or `python3 main.py`.

No external packages, Tkinter, or GUI required.

## Features

Restaurant browsing, food searching, sorting by price, cart management, undo last cart addition, checkout, saved customers/orders, order tracking, and FIFO processing of pending orders. Order processing is a simulation, not a real delivery service.

## DSA

- **Stack (LIFO):** `CartStack` uses list `append` / `pop` for cart undo.
- **Queue (FIFO):** `OrderQueue` uses `collections.deque` to process pending orders in arrival order.
- **Linear Search O(n):** `linear_search` matches food names.
- **Merge Sort O(n log n):** `merge_sort` sorts foods by price without built-in `sort`.
- **Hash Map average O(1):** `food_by_id` and `restaurant_by_id` dictionaries.

## OOP

`Person` is an abstract base class; `Customer` inherits it and implements `details()` (abstraction, inheritance, polymorphism). The phone number is a private attribute (encapsulation). Other classes: `Restaurant`, `FoodItem`, `CartStack`, `OrderQueue`, `FoodDeliverySystem`.

## Dataset files

- `restaurants.csv`: restaurant_id, name, location
- `food_items.csv`: food_id, name, price, restaurant_id, category
- `customers.csv`: name, phone
- `orders.csv`: order_id, customer, phone, items, total, status, date

The program reads datasets from its own folder and writes confirmed orders and new customers back to CSV. The `items` column stores food IDs separated by semicolons.
