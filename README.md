# Trigram Search with SQLite Database

This project demonstrates a trigram-based search implementation using an SQLite database. It allows users to search for products by name, category, or brand using trigrams.

## Overview

The system works by:

1.  Taking a user's search query.
2.  Generating trigrams from the query.
3.  Searching the database for products associated with those trigrams.
4.  Ranking the results based on the frequency of trigram matches.
5.  Displaying the top 10 results.

## Files

*   **`main.py`**: Contains the main application logic, including:
    *   `create_trigram(item: str)`: Function to generate trigrams from a given string.
    *   `DBItem` class: Represents a product item retrieved from the database.
    *   Main execution block:
        *   Connects to the SQLite database.
        *   Prompts the user for search queries.
        *   Performs the trigram search.
        *   Displays the results.
        *   Closes the database connection.

*   **`database.py`**: Contains the `SQLiteDatabase` class, which provides a wrapper around the `sqlite3` library for database interactions.  It offers methods for connecting to the database, executing queries (including batch queries), fetching single or multiple results, and closing the connection.

## Database Schema

The system expects the following tables in the SQLite database:

*   **`products`**:
    *   `id` (INTEGER PRIMARY KEY)
    *   `product_name` (TEXT)
    *   `price` (REAL)
    *   `description` (TEXT)
    *   `category` (TEXT)
    *   `brand` (TEXT)
    *   `stock_quantity` (INTEGER)
    *   `release_date` (TEXT)
    *   `rating` (REAL)

*   **`tags`**:
    *   `id` (INTEGER PRIMARY KEY)
    *   `tag` (TEXT, UNIQUE) - Contains the trigram strings.

*   **`product_tag_map`**:
    *   `product_id` (INTEGER) - Foreign key referencing `products.id`
    *   `tag_id` (INTEGER) - Foreign key referencing `tags.id`
    *   `count` (INTEGER) - Optional: Number of times a product is tagged with the same trigram

**Important:**  The database file name is hardcoded as `"products.db"` in `main.py`. The database is included as a zip file.

## How It Works

1.  **Trigram Generation:** The `create_trigram` function takes a string as input and generates all possible trigrams (sequences of three characters) from it.  It first lowercases the input and removes whitespace.

2.  **Database Search:** For each trigram generated from the user's query:
    *   It searches the `tags` table for a matching tag and retrieves its `id`.
    *   If the tag exists, it queries the `product_tag_map` table to find all `product_id`s associated with that `tag_id`, along with an optional count.
    *   The product IDs and counts are stored in a dictionary to track the frequency of each product being associated with the trigrams.
    *   The count from product_tag_map is optional and determines the "weight" of the trigram match with the product_id. If it's useful to know the count, keep it; otherwise, remove it.

3.  **Result Ranking:**  The results are ranked based on the frequency of product IDs appearing across all trigrams.

4.  **Display:** The top 10 results are fetched from the `products` table using the ranked product IDs and displayed to the user. Only `product_name`, `price`, `category`, and `brand` are shown.

## Usage

1.  **Database Setup:** Ensure you have an SQLite database named `products.db` with the tables and schema described above. Extract the database from the provided zip file.
2.  **Install Dependencies:** No external libraries are needed beyond the Python standard library.
3.  **Run the Script:** Execute the `main.py` script:

    ```bash
    python main.py
    ```

4.  **Search:** The script will prompt you to enter search queries. Type your query and press Enter. The top 10 matching products will be displayed.
5.  **Exit:** Type "exit" and press Enter to quit the program.

## Example Interaction
    python .\main.py
    Search DB: microsoft
    ('Microsoft Corporation', 991.03, 'Beauty', 'Centidel')
    ('Smith Micro Software, Inc.', 794.4, 'Home & Kitchen', 'Feedfish')
    ('Microsoft Corporation', 624.92, 'Toys & Games', 'Agimba')
    ('Smith Micro Software, Inc.', 254.07, 'Toys & Games', 'Yodo')
    ('Smith Micro Software, Inc.', 127.23, 'Books', 'Roombo')
    ('Smith Micro Software, Inc.', 27.65, 'Clothing', 'Reallinks')
    ('Microsoft Corporation', 572.14, 'Health & Personal Care', 'Yodoo')
    ('Microsoft Corporation', 95.52, 'Books', 'Ooba')
    ('Smith Micro Software, Inc.', 514.87, 'Books', 'Yata')
    ('Microsoft Corporation', 322.94, 'Books', 'Browsezoom')
