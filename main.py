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
    def cli_interface():
        while True:
            print("\n===== Restaurant Management System =====")
            print("1. Add New Dish")
            print("2. View All Dishes")
            print("3. Update Dish Info")
            print("4. Delete Dish")
            print("5. Exit System")
            print("========================================")
            choice = input("Please enter your choice (1-5): ")

            if choice == '1':
                name = input("Enter dish name: ")
                price = float(input("Enter dish price: "))
                category = input("Enter dish category: ")
                add_dish(name, price, category)
                print("✅ Dish added successfully!")
            elif choice == '2':
                dishes = get_all_dishes()
                if not dishes:
                    print("❌ No dishes found in the system.")
                    continue
                print("\n📋 All Dishes:")
                print(f"{'ID':<4} {'Name':<20} {'Price':<10} {'Category'}")
                print("-" * 50)
                for dish in dishes:
                    print(f"{dish['id']:<4} {dish['name']:<20} ${dish['price']:<9} {dish['category']}")
            elif choice == '3':
                dish_id = int(input("Enter dish ID to update: "))
                name = input("Enter new name (leave blank to keep): ")
                price_input = input("Enter new price (leave blank to keep): ")
                category = input("Enter new category (leave blank to keep): ")
                new_data = {}
                if name:
                    new_data['name'] = name
                if price_input:
                    new_data['price'] = float(price_input)
                if category:
                    new_data['category'] = category
                if update_dish(dish_id, new_data):
                    print("✅ Dish updated successfully!")
                else:
                    print("❌ Dish not found.")
            elif choice == '4':
                dish_id = int(input("Enter dish ID to delete: "))
                if delete_dish(dish_id):
                    print("✅ Dish deleted successfully!")
                else:
                    print("❌ Dish not found.")
            elif choice == '5':
                print("👋 Thank you for using the system. Goodbye!")
                break
            else:
                print("❌ Invalid choice! Please enter a number between 1-5.")

    if __name__ == "__main__":
        cli_interface()
if __name__ == "__main__":
    cli_interface()