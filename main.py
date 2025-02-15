from database import SQLiteDatabase

def create_trigram(item : str) -> list:
    item = item.lower()
    item = (item
            .replace(" ", '')
            .replace("\n", '')
            .replace("\t", '')
    )
    result = []
    for i in range(len(item)-2):
        result.append(item[i:i+3])
    return result

class DBItem:
    def __init__(self, id, product_name, price, description, category, brand, stock_quantity, release_date, rating):
        self.id = id
        self.name = product_name
        self.price = price
        self.description = description
        self.category = category
        self.brand = brand
        self.stock_quantity = stock_quantity
        self.release_date = release_date
        self.rating = rating
    def __str__(self):
        return f"{self.id}, {self.name}, {self.price}, {self.description}, {self.category}, {self.brand}, {self.stock_quantity}, {self.release_date}, {self.rating}"


if __name__ == "__main__":
    db = SQLiteDatabase("products.db")

    user_query = ""
    while 1:
        user_query = input("Search DB: ")
        if user_query == "exit":
            break

        trigrams = create_trigram(user_query)
        res = {}
        for trigram in trigrams:
            # Get IDs for all tags
            tag_id = db.fetch_one("SELECT id FROM tags WHERE tag = ?", [trigram])
            if tag_id is None:
                continue
            product_ids = db.fetch_all("SELECT product_id, count FROM product_tag_map WHERE tag_id = ?", [tag_id[0]])
            product_map = {}
            for product_id in product_ids:
                if product_id[0] in product_map:
                    product_map[product_id[0]] += product_id[1]
                else:
                    product_map[product_id[0]] = product_id[1]
            for k, v in product_map.items():
                if k in res:
                    res[k] += v
                else:
                    res[k] = v
        res = sorted(res.items(), key=lambda x: x[1], reverse=True)[:10]
        for key in res:
            print(db.fetch_one("SELECT product_name, price, category, brand FROM products WHERE id = ?", [key[0]]))

    db.close_connection()
