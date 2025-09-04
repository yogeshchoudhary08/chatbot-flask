from flask import Flask, request
import requests
import sqlite3
import os
def save_order(order):
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO orders (name, contact, product_name, price, address)
        VALUES (?, ?, ?, ?, ?)
    ''', (order['name'], order['contact'], order['product']['name'], order['product']['price'], order['address']))
    conn.commit()
    conn.close()

def init_db():
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS orders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            contact TEXT,
            product_name TEXT,
            price INTEGER,
            address TEXT
        )
    ''')
    conn.commit()
    conn.close()

init_db()

app = Flask(__name__)

PAGE_ACCESS_TOKEN = 'YOUR_PAGE_ACCESS_TOKEN'
VERIFY_TOKEN = 'YOUR_VERIFY_TOKEN'
ADMIN_USER_ID = 'YOUR_ADMIN_MESSENGER_USER_ID'

user_states = {}
user_order_data = {}

brands = {
    "1": {
        "name": "Brand A",
        "products": {
            "1": {
                "name": "Whey Protein",
                "price": 4500,
                "desc": "High quality protein powder",
                "stock": 20,
                "image_url": "https://example.com/whey.jpg"
            },
            "2": {
                "name": "Energy Bar",
                "price": 300,
                "desc": "Nutritious energy bar",
                "stock": 50,
                "image_url": "https://example.com/energybar.jpg"
            }
        }
    },
    "2": {
        "name": "Brand B",
        "products": {
            "1": {
                "name": "Creatine",
                "price": 1200,
                "desc": "Performance enhancing supplement",
                "stock": 15,
                "image_url": "https://example.com/creatine.jpg"
            }
        }
    }
}


def send_message(user_id, message_text):
    url = f"https://graph.facebook.com/v17.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "messaging_type": "RESPONSE",
        "recipient": {"id": user_id},
        "message": {"text": message_text}
    }
    requests.post(url, json=payload)

def send_image_with_caption(user_id, image_url, caption):
    url = f"https://graph.facebook.com/v17.0/me/messages?access_token={PAGE_ACCESS_TOKEN}"
    payload = {
        "messaging_type": "RESPONSE",
        "recipient": {"id": user_id},
        "message": {
            "attachment": {
                "type": "image",
                "payload": {
                    "url": image_url,
                    "is_reusable": True
                }
            },
            "text": caption
        }
    }
    requests.post(url, json=payload)

def notify_admin(order):
    message = (f"New Order Received:\n"
               f"Name: {order['name']}\n"
               f"Contact: {order['contact']}\n"
               f"Product: {order['product']['name']}\n"
               f"Price: ₹{order['product']['price']}\n"
               f"Address: {order['address']}")
    send_message(ADMIN_USER_ID, message)

@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        if request.args.get('hub.mode') == 'subscribe' and request.args.get('hub.challenge'):
            if request.args.get('hub.verify_token') == VERIFY_TOKEN:
                return request.args.get('hub.challenge'), 200
            else:
                return 'Verification token mismatch', 403
        return 'Hello world', 200

    elif request.method == 'POST':
        data = request.json
        if data.get('entry'):
            for entry in data['entry']:
                messaging_events = entry.get('messaging', [])
                for event in messaging_events:
                    sender_id = event['sender']['id']
                    if event.get('message') and 'text' in event['message']:
                        message_text = event['message']['text']
                        handle_message(sender_id, message_text)
        return 'OK', 200

def handle_message(user_id, message):
    state = user_states.get(user_id, "welcome")

    if state == "welcome":
        welcome_msg = "Welcome to Chaudhry Supplement Hub! Please select a brand:\n" + \
                      "\n".join(f"{key}. {value['name']}" for key, value in brands.items())
        send_message(user_id, welcome_msg)
        user_states[user_id] = "brand_selection"

    elif state == "brand_selection":
        if message.strip() in brands:
            brand_id = message.strip()
            user_states[user_id] = f"product_selection:{brand_id}"
            product_list = brands[brand_id]["products"]
            product_msg = f"You selected {brands[brand_id]['name']}. Choose a product:\n" + \
                          "\n".join(f"{key}. {val['name']}" for key, val in product_list.items())
            send_message(user_id, product_msg)
        else:
            send_message(user_id, "Invalid brand. Please select a valid brand number.")

    elif state.startswith("product_selection:"):
        brand_id = state.split(":")[1]
        products = brands[brand_id]["products"]
        if message.strip() in products:
            product_id = message.strip()
            product = products[product_id]
            caption = f"{product['name']} - ₹{product['price']}\n{product['desc']}\nIn stock: {product['stock']}\nReply YES to buy or NO to go back."
            send_image_with_caption(user_id, product['image_url'], caption)
            user_states[user_id] = f"confirm_purchase:{brand_id}:{product_id}"
        else:
            send_message(user_id, "Invalid product. Please select a valid product number.")

    elif state.startswith("confirm_purchase:"):
        parts = state.split(":")
        brand_id, product_id = parts[1], parts[2]
        if message.strip().lower() == "yes":
            send_message(user_id, "Please provide your name for the order:")
            user_states[user_id] = f"collect_name:{brand_id}:{product_id}"
        elif message.strip().lower() == "no":
            send_message(user_id, "Okay, please select a brand:\n" +
                         "\n".join(f"{key}. {value['name']}" for key, value in brands.items()))
            user_states[user_id] = "brand_selection"
        else:
            send_message(user_id, "Reply YES to buy or NO to go back.")

    elif state.startswith("collect_name:"):
        parts = state.split(":")
        brand_id, product_id = parts[1], parts[2]
        user_order_data[user_id] = {"name": message.strip(), "brand": brands[brand_id]["name"], "product": brands[brand_id]["products"][product_id]}
        send_message(user_id, "Thanks! Please provide your contact number:")
        user_states[user_id] = f"collect_contact:{brand_id}:{product_id}"

    elif state.startswith("collect_contact:"):
        parts = state.split(":")
        brand_id, product_id = parts[1], parts[2]
        user_order_data[user_id]["contact"] = message.strip()
        send_message(user_id, "Please provide your address:")
        user_states[user_id] = f"collect_address:{brand_id}:{product_id}"

    elif state.startswith("collect_address:"):
        parts = state.split(":")
        brand_id, product_id = parts[1], parts[2]
        user_order_data[user_id]["address"] = message.strip()
        
        order = user_order_data[user_id]
        summary = (f"Order Summary:\n"
                   f"Name: {order['name']}\n"
                   f"Contact: {order['contact']}\n"
                   f"Product: {order['product']['name']}\n"
                   f"Price: ₹{order['product']['price']}\n"
                   f"Address: {order['address']}\n\n"
                   f"Thank you for your order! We will contact you soon.")
        send_message(user_id, summary)
        
        save_order(order)
        notify_admin(order)
        
        user_states[user_id] = "welcome"  # Reset for new conversation

    else:
        send_message(user_id, "Sorry, I didn't understand that. Please select a brand or type HELP for assistance.")


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
