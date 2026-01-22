import os

DATA_FILE = "restaurant_data.txt"

def init_data_file():
    if not os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            pass

def add_dish(name, price, category):
    init_data_file()
    dishes = get_all_dishes()
    dish_id = max([d['id'] for d in dishes], default=0) + 1
    new_dish = {'id': dish_id, 'name': name, 'price': price, 'category': category}
    dishes.append(new_dish)
    save_dishes(dishes)
    return new_dish

def get_all_dishes():
    init_data_file()
    dishes = []
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                dish = eval(line.strip())
                dishes.append(dish)
    return dishes

def save_dishes(dishes):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        for dish in dishes:
            f.write(f"{dish}\n")

def update_dish(dish_id, new_data):
    dishes = get_all_dishes()
    for dish in dishes:
        if dish['id'] == dish_id:
            dish.update(new_data)
            save_dishes(dishes)
            return True
    return False

def delete_dish(dish_id):
    dishes = get_all_dishes()
    new_dishes = [d for d in dishes if d['id'] != dish_id]
    if len(new_dishes) != len(dishes):
        save_dishes(new_dishes)
        return True
    return False
def cli_interface():
    while True:
        print("\n1. Add Dish")
        print("2. View All Dishes")
        print("3. Update Dish")
        print("4. Delete Dish")
        print("5. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            name = input("Enter dish name: ")
            price = float(input("Enter dish price: "))
            category = input("Enter dish category: ")
            add_dish(name, price, category)
            print("Dish added successfully.")
        elif choice == '2':
            dishes = get_all_dishes()
            if not dishes:
                print("No dishes found.")
                continue
            for dish in dishes:
                print(f"ID: {dish['id']}, Name: {dish['name']}, Price: {dish['price']}, Category: {dish['category']}")
        elif choice == '3':
            dish_id = int(input("Enter dish ID to update: "))
            name = input("Enter new dish name (leave blank to keep current): ")
            price_input = input("Enter new dish price (leave blank to keep current): ")
            category = input("Enter new dish category (leave blank to keep current): ")
            new_data = {}
            if name:
                new_data['name'] = name
            if price_input:
                new_data['price'] = float(price_input)
            if category:
                new_data['category'] = category
            if update_dish(dish_id, new_data):
                print("Dish updated successfully.")
            else:
                print("Dish not found.")
        elif choice == '4':
            dish_id = int(input("Enter dish ID to delete: "))
            if delete_dish(dish_id):
                print("Dish deleted successfully.")
            else:
                print("Dish not found.")
        elif choice == '5':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    cli_interface():