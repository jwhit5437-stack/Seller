# ...existing code...
# Seller-Buyer interactive checker (user as buyer)

seller_name = "Aung Store"          # String

# Ask the user to be the buyer
buyer_name = input("Your name: ").strip() or "Guest"  
buyer_password = input("Your Password: ").strip() or "Guest" # String
try:
    buyer_balance = float(input("Starting balance (e.g. 2000): ") or 2000.0)  # Float
except ValueError:
    buyer_balance = 2000.0

inventory = [
    {"name": "Smartphone", "quantity": 5,  "price": 299.99},
    {"name": "Computer",   "quantity": 2,  "price": 850.50},
    {"name": "Mouse",      "quantity": 10, "price": 19.99},
    {"name": "Keyboard",   "quantity": 5,  "price": 49.99},
]

def show_inventory():
    print(f"Seller: {seller_name}")
    print("---------------------------------")
    for idx, it in enumerate(inventory, start=1):
        in_stock = it["quantity"] > 0  # Boolean
        status = "In Stock" if in_stock else "Out of Stock"
        print(f"{idx:2}. {it['name']:12} | Qty: {it['quantity']:2} | ${it['price']:.2f} | {status}")
    print("---------------------------------")

def find_item_by_name(name):
    for it in inventory:
        if it["name"].lower() == name.lower():
            return it
    return None

def attempt_purchase(buyer, item, want_qty, is_member=False):
    # item may be item dict
    if item is None:
        print("Item not found.")
        return False
    qty = int(item["quantity"])
    price = float(item["price"])
    in_stock = qty > 0
    if not in_stock:
        print(f"'{item['name']}' is out of stock.")
        return False
    if want_qty <= 0:
        print("Quantity must be at least 1.")
        return False
    if want_qty > qty:
        print(f"Not enough '{item['name']}' in stock. Available: {qty}.")
        return False
    total = want_qty * price
    discount = 0.0
    if is_member:
        discount = 0.10 * total
    final = total - discount
    global buyer_balance
    if buyer_balance < final:
        print(f"{buyer} does not have enough balance. Needed ${final:.2f}, has ${buyer_balance:.2f}.")
        return False
    # complete sale
    item["quantity"] -= want_qty
    buyer_balance -= final
    print(f"{buyer} purchased {want_qty} x {item['name']} for ${final:.2f} (discount ${discount:.2f}).")
    return True

def bulk_purchase(buyer):
    """
    Buy up to 4 different items in one transaction.
    Collect selections first, validate stock and funds, then complete atomically.
    """
    show_inventory()
    try:
        count = int(input("How many different items do you want to buy? (1-4): ").strip())
    except ValueError:
        print("Invalid number.")
        return
    if count < 1 or count > 4:
        print("Please choose between 1 and 4 items.")
        return

    selections = []  # list of (item_dict, qty)
    for i in range(count):
        sel = input(f"[{i+1}/{count}] Enter item number or name (or 'c' to cancel): ").strip()
        if sel.lower() == 'c':
            print("Bulk purchase cancelled.")
            return
        item = None
        if sel.isdigit():
            idx = int(sel) - 1
            if 0 <= idx < len(inventory):
                item = inventory[idx]
        if item is None:
            item = find_item_by_name(sel)
        if item is None:
            print("Item not found. Try again.")
            return
        # Prevent duplicate item selection
        if any(it is item for it, _ in selections):
            print("Item already selected. Choose a different item.")
            return
        try:
            want_qty = int(input(f"Enter quantity of '{item['name']}' to buy: ").strip())
        except ValueError:
            print("Invalid quantity.")
            return
        if want_qty <= 0:
            print("Quantity must be at least 1.")
            return
        selections.append((item, want_qty))

    mem = input("Are you a member? (y/N): ").strip().lower()
    is_member = mem == 'y'

    # Validate stock availability
    for item, q in selections:
        if q > item["quantity"]:
            print(f"Not enough '{item['name']}' in stock. Available: {item['quantity']}. Transaction cancelled.")
            return

    # Calculate totals
    total = sum(q * float(item["price"]) for item, q in selections)
    discount = 0.10 * total if is_member else 0.0
    final = total - discount

    global buyer_balance
    if buyer_balance < final:
        print(f"Not enough balance. Needed ${final:.2f}, have ${buyer_balance:.2f}. Transaction cancelled.")
        return

    # Complete sale atomically
    for item, q in selections:
        item["quantity"] -= q
    buyer_balance -= final

    print("\nPurchase successful. Receipt:")
    print("---------------------------------")
    for item, q in selections:
        line_total = q * float(item["price"])
        print(f"{q} x {item['name']:12} @ ${item['price']:.2f} = ${line_total:.2f}")
    print(f"Subtotal: ${total:.2f}")
    if is_member:
        print(f"Member discount: -${discount:.2f}")
    print(f"Total paid: ${final:.2f}")
    print("---------------------------------")

def main_loop():
    print(f"Welcome, {buyer_name}! Your balance: ${buyer_balance:.2f}")
    while True:
        print("\nOptions: [1] Show inventory  [2] Buy single item  [3] Buy multiple items  [4] Show balance  [5] Quit")
        choice = input("Choose option: ").strip()
        if choice == "1":
            show_inventory()
        elif choice == "2":
            show_inventory()
            sel = input("Enter item number or name to buy (or 'c' to cancel): ").strip()
            if sel.lower() == 'c':
                continue
            item = None
            # try parse number
            if sel.isdigit():
                idx = int(sel) - 1
                if 0 <= idx < len(inventory):
                    item = inventory[idx]
            if item is None:
                item = find_item_by_name(sel)
            if item is None:
                print("Item not found.")
                continue
            try:
                want_qty = int(input(f"Enter quantity of '{item['name']}' to buy: ").strip())
            except ValueError:
                print("Invalid quantity.")
                continue
            mem = input("Are you a member? (y/N): ").strip().lower()
            is_member = mem == 'y'
            attempt_purchase(buyer_name, item, want_qty, is_member)
        elif choice == "3":
            bulk_purchase(buyer_name)
        elif choice == "4":
            print(f"{buyer_name}'s balance: ${buyer_balance:.2f}")
        elif choice == "5":
            print("Exiting. Final inventory and balance:")
            show_inventory()
            print(f"{buyer_name}'s remaining balance: ${buyer_balance:.2f}")
            break
        else:
            print("Invalid option. Choose 1-5.")

if __name__ == "__main__":
    main_loop()
# ...existing