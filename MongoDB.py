from pymongo import MongoClient

def main():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['CitySustainability']

    collections = {
        '1': 'WaterConsumption',
        # Add your other collections here
    }

    while True:
        print("\nSelect a collection:")
        for key, value in collections.items():
            print(f"{key}. {value}")
        print("6. Exit")

        choice = input("Enter choice: ")

        if choice == '6':
            break
        elif choice in collections:
            collection_name = collections[choice]
            collection = db[collection_name]
            collection_menu(collection)
        else:
            print("Invalid choice.")

def collection_menu(collection):
    while True:
        print(f"\nCollection: {collection.name}")
        print("1. Display all documents")
        print("2. Add new document")
        print("3. Update existing document")
        print("4. Delete existing document")
        print("5. Search documents")
        print("6. Back to main menu")

        choice = input("Enter choice: ")

        if choice == '1':
            display_documents(collection)
        elif choice == '2':
            add_document(collection)
        elif choice == '3':
            update_document(collection)
        elif choice == '4':
            delete_document(collection)
        elif choice == '5':
            search_documents(collection)
        elif choice == '6':
            break
        else:
            print("Invalid choice.")

def display_documents(collection):
    documents = collection.find()
    for doc in documents:
        print(doc)

def add_document(collection):
    # Example for WaterConsumption
    year = int(input("Enter year: "))
    location_code = input("Enter location code: ")
    location_name = input("Enter location name: ")
    statistic_code = input("Enter statistic code: ")
    statistic_label = input("Enter statistic label: ")
    unit = input("Enter unit: ")
    value = float(input("Enter value: "))

    document = {
        "year": year,
        "location": {
            "code": location_code,
            "name": location_name
        },
        "consumption": [
            {
                "statistic_code": statistic_code,
                "statistic_label": statistic_label,
                "unit": unit,
                "value": value
            }
        ]
    }

    collection.insert_one(document)
    print("Document added successfully.")

def update_document(collection):
    year = int(input("Enter year of the document to update: "))
    location_code = input("Enter location code of the document to update: ")

    # Find the document
    doc = collection.find_one({ "year": year, "location.code": location_code })

    if doc:
        print("Current document:", doc)
        # Update fields as needed
        new_value = float(input("Enter new value for the first consumption statistic: "))
        collection.update_one(
            { "_id": doc["_id"] },
            { "$set": { "consumption.0.value": new_value } }
        )
        print("Document updated successfully.")
    else:
        print("Document not found.")

def delete_document(collection):
    year = int(input("Enter year of the document to delete: "))
    location_code = input("Enter location code of the document to delete: ")

    result = collection.delete_one({ "year": year, "location.code": location_code })

    if result.deleted_count > 0:
        print("Document deleted successfully.")
    else:
        print("Document not found.")

def search_documents(collection):
    search_term = input("Enter location name to search: ")
    documents = collection.find({ "location.name": { "$regex": search_term, "$options": 'i' } })
    for doc in documents:
        print(doc)

if __name__ == "__main__":
    main()

