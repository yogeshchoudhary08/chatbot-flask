#include <iostream>
#include <vector>
#include <string>
using namespace std;

class Product {
public:
    int id;
    string name;
    int quantity;
    double price;

    Product(int pid, string pname, int qty, double pr) : id(pid), name(pname), quantity(qty), price(pr) {}
};

vector<Product> inventory;

void addProduct() {
    int id, quantity;
    double price;
    string name;
    cout << "Enter product ID: ";
    cin >> id;
    cin.ignore();
    cout << "Enter product name: ";
    getline(cin, name);
    cout << "Enter quantity: ";
    cin >> quantity;
    cout << "Enter price: ";
    cin >> price;

    Product p(id, name, quantity, price);
    inventory.push_back(p);
    cout << "Product added successfully.\n";
}

void displayProducts() {
    if(inventory.empty()) {
        cout << "Inventory is empty.\n";
        return;
    }
    for (auto &p : inventory) {
        cout << "ID: " << p.id << ", Name: " << p.name 
             << ", Quantity: " << p.quantity << ", Price: " << p.price << endl;
    }
}

int main() {
    int choice;
    do {
        cout << "\nInventory Management System\n";
        cout << "1. Add Product\n2. Display Products\n3. Exit\n";
        cout << "Enter your choice: ";
        cin >> choice;

        switch(choice) {
            case 1: addProduct(); break;
            case 2: displayProducts(); break;
            case 3: cout << "Exiting program.\n"; break;
            default: cout << "Invalid choice. Try again.\n"; 
        }
    } while(choice != 3);

    return 0;
}
