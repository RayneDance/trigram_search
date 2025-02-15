# Trigram Search with SQLite Database

This project demonstrates a trigram-based search implementation using an SQLite database. It allows users to search for products by name, category, or brand using trigrams.

## Overview

The system works by:

1.  Taking a user's search query.
2.  Generating trigrams from the query.
3.  Searching the database for products associated with those trigrams.
4.  Ranking the results based on the frequency of trigram matches.
5.  Displaying the top 10 results.

**Key Idea:** Instead of generating trigrams on the fly during searches, the trigrams are pre-computed and stored in the database, significantly speeding up the search process.

## Files

*   **`main.py`**: Contains the main application logic, including:
    *   `create_trigram(item: str)`: Function to generate trigrams from a given string.
    *   `DBItem` class: Represents a product item retrieved from the database.
    *   Main execution block:
        *   Connects to the SQLite database.
        *   Prompts the user for search queries.
        *   Generates trigrams from the user's input.
        *   Searches the database for products associated with these trigrams using the pre-computed trigram index.
        *   Ranks and displays the results.
        *   Closes the database connection.

*   **`database.py`**: Contains the `SQLiteDatabase` class, which provides a wrapper around the `sqlite3` library for database interactions.  It offers methods for connecting to the database, executing queries (including batch queries), fetching single or multiple results, and closing the connection.

## Database Schema

The system relies on the following tables in the SQLite database:

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

## How It Works (Detailed Explanation)

1.  **Pre-processing and Indexing:**  The core idea is to pre-process the `products` data to create a trigram index:
    *   For each row in the `products` table, the `product_name`, `category`, and `brand` fields are processed.  The `description` field is *not* included in the trigram generation.
    *   For each of these fields, trigrams (sequences of three characters) are generated.
    *   Each unique trigram is added to the `tags` table. This table effectively becomes a vocabulary of trigrams present in the product data.
    *   For each product, an entry is created in the `product_tag_map` table to link the `product_id` with each `tag_id` (representing a trigram) found in its `product_name`, `category`, or `brand`.  The `count` field in `product_tag_map` (if used) stores the number of times that trigram occurs within those fields for that specific product. This count can be used to weight the importance of the trigram match.

2.  **Search Process:**
    *   The user enters a search query.
    *   The `create_trigram` function generates trigrams from the query string, similar to the pre-processing step.
    *   For each trigram:
        *   The `tags` table is queried to find the corresponding `tag_id`.
        *   If the `tag_id` is found, the `product_tag_map` table is queried to retrieve all `product_id`s associated with that `tag_id`, along with the optional `count`.
    *   The results are aggregated, and products are ranked based on the frequency of their associated `product_id` appearing across the matched trigrams. The `count` field in `product_tag_map` can be incorporated into this ranking process to give more weight to products with more frequent trigram matches.

3.  **Result Ranking and Display:**  The top 10 products, ranked by trigram match frequency, are retrieved from the `products` table and displayed to the user.

## Usage

1.  **Database Setup:** Ensure you have an SQLite database named `products.db` with the tables and schema described above. Extract the database from the provided zip file. This database should already contain the `products`, `tags`, and `product_tag_map` tables populated as described in the "How It Works" section.
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