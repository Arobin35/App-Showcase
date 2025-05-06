from fastapi import FastAPI, HTTPException, Body
from pydantic import BaseModel
import sqlite3
from typing import Optional
import datetime
from datetime import date
import os
from urllib.parse import unquote

app = FastAPI()

# -------------------- DATABASE CONNECTION -------------------- #

import sqlite3

def get_db_connection():
    conn = sqlite3.connect("pantry.db", check_same_thread=False, timeout = 10)
    conn.row_factory = sqlite3.Row
    return conn


# -------------------- DATA MODELS -------------------- #

class FoodItem(BaseModel):
    id: int | None = None
    name: str
    quantity: int
    expiration_date: date
    user_id: str

class UserLogin(BaseModel):
    name: str
    password: str

class User(BaseModel):
    username: str
    email: Optional[str] = None
    phone: Optional[str] = None
    password_hash: str
    profile_picture: Optional[str] = None
    family_id: Optional[str] = None
    created_at: str  # ✅ Expecting an ISO 8601 string
    
class SharedListItem(BaseModel):
    name: str
    family_id: Optional[str] = None
    added_by_user_id: int
    timestamp: str  # ISO 8601 format
    notes: Optional[str] = None

    
class VerifyUserRequest(BaseModel):
    identifier: str  # ✅ Accepts username OR email
    
class UpdateFoodItemRequest(BaseModel):
    quantity: int
    expiration_date: str  # ✅ Now included
    
class UpdatePantryItemRequest(BaseModel):
    quantity: int
    expiration_date: str  # ✅ Now included
    
class UpdateQuantityRequest(BaseModel):
    quantity: int

# -------------------- FRIDGE ITEMS ENDPOINTS -------------------- #

@app.get("/food_items/{user_id}")
def get_fridge_items(user_id: str):
    """Get all food items for a specific user."""
    conn = get_db_connection()
    items = conn.execute("SELECT id, name, quantity, expiration_date, CAST(user_id AS INTEGER) as user_id FROM food_items WHERE user_id = ?", (user_id,)).fetchall()
    conn.close()
    return {"food_items": [dict(item) for item in items]}


@app.post("/food_items", status_code=201)
def add_fridge_item(item: FoodItem):
    """Add a new food item for a specific user."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # ✅ Debugging: Print received data before inserting
    print(f"📡 Adding food item: user_id={item.user_id}, name={item.name}, quantity={item.quantity}, expiration={item.expiration_date}")

    try:
        # ✅ Ensure correct user_id type (remove unnecessary conversion)
        print("🔍 SQL Query: INSERT INTO food_items (user_id, name, quantity, expiration_date) VALUES (?, ?, ?, ?)")

        cursor.execute(
            "INSERT INTO food_items (user_id, name, quantity, expiration_date) VALUES (?, ?, ?, ?)",
            (item.user_id, item.name, item.quantity, item.expiration_date)
        )

        conn.commit()
        print("✅ Successfully inserted item into database.")  # ✅ Debugging
        conn.close()
        return {"message": "Food item added successfully!"}

    except sqlite3.Error as e:
        print(f"❌ Database Error: {str(e)}")  # ✅ Debugging to see the exact SQLite error
        conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

    
    
@app.delete("/food_items/{name}")
def delete_fridge_item(name: str, user_id: str):
    """Delete a food item by name for a user."""
    conn = get_db_connection()
    cursor = conn.cursor()

    print(f"🗑️ Attempting to delete '{name}' for user {user_id}")  # Debugging

    cursor.execute(
        "DELETE FROM food_items WHERE name = ? AND user_id = ?",
        (name, user_id)
    )
    conn.commit()

    if cursor.rowcount == 0:
        print("❌ Delete failed: No matching item found!")  # Debugging
        conn.close()
        raise HTTPException(status_code=404, detail="Food item not found")

    print("✅ Successfully deleted item")  # Debugging
    conn.close()
    return {"message": f"Food item '{name}' deleted successfully!"}

    

@app.patch("/food_items/{item_id}/{user_id}")
def update_fridge_item(item_id: int, user_id: str, request: UpdateFoodItemRequest):
    """Update quantity and expiration date of a food item for a user."""
    conn = get_db_connection()
    cursor = conn.cursor()

    print(f"🔹 Updating food item {item_id} for user {user_id} -> Quantity: {request.quantity}, Expiration: {request.expiration_date}")  # Debugging

    cursor.execute(
        """
        UPDATE food_items 
        SET quantity = ?, expiration_date = ? 
        WHERE id = ? AND user_id = ?
        """,
        (request.quantity, request.expiration_date, item_id, user_id)
    )
    conn.commit()

    if cursor.rowcount == 0:
        print("❌ Update failed: No rows affected")  # Debugging
        conn.close()
        raise HTTPException(status_code=404, detail="Food item not found")

    print("✅ Update applied successfully")  # Debugging
    conn.close()
    return {"message": "Food item updated successfully!"}






# -------------------- PANTRY ITEMS ENDPOINTS -------------------- #

@app.get("/pantry_items/{user_id}")
def get_pantry_items(user_id: str):
    """Get all pantry items for a specific user."""
    conn = get_db_connection()
    items = conn.execute("SELECT id, name, quantity, expiration_date, CAST(user_id AS INTEGER) as user_id FROM pantry_items WHERE user_id = ?", (user_id,)).fetchall()
    conn.close()
    return {"food_items": [dict(item) for item in items]}





@app.post("/pantry_items", status_code=201)
def add_pantry_item(item: FoodItem):
    """Add a new pantry item for a specific user."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # ✅ Debugging: Print received data before inserting
    print(f"📡 Adding pantry item: user_id={item.user_id}, name={item.name}, quantity={item.quantity}, expiration={item.expiration_date}")

    try:
        print("🔍 SQL Query: INSERT INTO pantry_items (user_id, name, quantity, expiration_date) VALUES (?, ?, ?, ?)")

        cursor.execute(
            "INSERT INTO pantry_items (user_id, name, quantity, expiration_date) VALUES (?, ?, ?, ?)",
            (item.user_id, item.name, item.quantity, item.expiration_date)
        )

        conn.commit()
        print("✅ Successfully inserted item into pantry_items table.")
        conn.close()
        return {"message": "Pantry item added successfully!"}

    except sqlite3.Error as e:
        print(f"❌ Database Error: {str(e)}")
        conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


    
    
    

@app.patch("/pantry_items/{item_id}/{user_id}")
def update_pantry_item(item_id: int, user_id: str, request: UpdateFoodItemRequest):
    """Update quantity and expiration date of a food item for a user."""
    conn = get_db_connection()
    cursor = conn.cursor()

    print(f"🔹 Updating Pantry item {item_id} for user {user_id} -> Quantity: {request.quantity}, Expiration: {request.expiration_date}")  # Debugging

    cursor.execute(
        """
        UPDATE pantry_items 
        SET quantity = ?, expiration_date = ? 
        WHERE id = ? AND user_id = ?
        """,
        (request.quantity, request.expiration_date, item_id, user_id)
    )
    conn.commit()

    if cursor.rowcount == 0:
        print("❌ Update failed: No rows affected")  # Debugging
        conn.close()
        raise HTTPException(status_code=404, detail="Food item not found")

    print("✅ Update applied successfully")  # Debugging
    conn.close()
    return {"message": "Food item updated successfully!"}
    
    
    
    
@app.delete("/pantry_items/{name}")
def delete_pantry_item(name: str, user_id: str):
    """Delete a pantry item by name for a user."""
    conn = get_db_connection()
    cursor = conn.cursor()

    print(f"🗑️ Attempting to delete '{name}' for user {user_id}")  # Debugging

    cursor.execute(
        "DELETE FROM pantry_items WHERE name = ? AND user_id = ?",
        (name, user_id)
    )
    conn.commit()

    if cursor.rowcount == 0:
        print("❌ Delete failed: No matching item found!")  # Debugging
        conn.close()
        raise HTTPException(status_code=404, detail="Pantry item not found")

    print("✅ Successfully deleted item")  # Debugging
    conn.close()
    return {"message": f"Pantry item '{name}' deleted successfully!"}










# -------------------- USER MANAGEMENT -------------------- #

@app.post("/users", status_code=201)
def add_user(user: User):
    """Add a new user, ensuring unique phone numbers."""
    conn = get_db_connection()
    cursor = conn.cursor()

    # ✅ Check if phone number already exists
    cursor.execute("SELECT 1 FROM users WHERE phone = ?", (user.phone,))
    existing_phone = cursor.fetchone()

    if existing_phone:
        conn.close()
        raise HTTPException(status_code=400, detail="Phone number already in use.")

    try:
        sql_query = """
        INSERT INTO users (username, email, phone, password_hash, profile_picture, family_id, created_at) 
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        cursor.execute(
            sql_query,
            (user.username, user.email, user.phone, user.password_hash, user.profile_picture, user.family_id, user.created_at),
        )
        conn.commit()
        conn.close()
        return {"message": "User added successfully!", "user_id": cursor.lastrowid}

    except sqlite3.IntegrityError as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Database error: {e}")




@app.post("/verify_user_exists")
def verify_user_exists(request: VerifyUserRequest):
    """Check if a user already exists."""
    conn = get_db_connection()
    cursor = conn.cursor()

    query = "SELECT 1 FROM users WHERE username = ? OR email = ?"
    cursor.execute(query, (request.identifier, request.identifier))  # ✅ Checks both username & email
    result = cursor.fetchone()
    conn.close()

    return {"exists": bool(result)}
    
    
    
@app.get("/users/{identifier}")
def get_user(identifier: str):
    """Retrieve user details by username, email, or user_id."""
    decoded_identifier = unquote(identifier)  # ✅ Decode %23 back to #
    conn = get_db_connection()
    cursor = conn.cursor()

    # ✅ Ensure `user_id` is returned as `id`
    if identifier.isdigit():
        query = "SELECT user_id AS id, username, email, password_hash, profile_picture, family_id, created_at FROM users WHERE user_id = ?"
        cursor.execute(query, (int(identifier),))
    else:
        query = "SELECT user_id AS id, username, email, password_hash, profile_picture, family_id, created_at FROM users WHERE username = ? OR email = ?"
        cursor.execute(query, (decoded_identifier, decoded_identifier))

    user = cursor.fetchone()
    conn.close()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return dict(user)  # ✅ `id` will now exist in response



        
@app.get("/get_user_id")
def get_user_id(identifier: str):
    """Retrieve the user ID based on username or email."""
    decoded_identifier = unquote(identifier)  # ✅ Decode %23 back to #

    print(f"📡 Decoded Identifier: {decoded_identifier}")  # ✅ Debugging log

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT user_id FROM users WHERE username = ? OR email = ?", (decoded_identifier, decoded_identifier))
    user = cursor.fetchone()

    if user:
        print(f"✅ Found User ID: {user['user_id']}")  # ✅ Debugging log
        conn.close()
        return {"user_id": user["user_id"]}
    else:
        print("❌ User not found in database!")  # ✅ Debugging log
        conn.close()
        raise HTTPException(status_code=404, detail="User not found")
        

        # -------------------- LIST MANAGEMENT -------------------- #
@app.get("/shared_list_items")
def get_shared_list_items(user_id: Optional[int] = None, family_id: Optional[str] = None):
    from urllib.parse import unquote
    conn = get_db_connection()
    try:
        cursor = conn.cursor()

        if family_id:
            family_id = unquote(family_id)  # ✅ Decode URL-encoded symbols like %23 -> #
            print(f"🔍 Decoded family_id: {family_id}")
            items = cursor.execute(
                "SELECT * FROM shared_list_items WHERE family_id = ?", (family_id,)
            ).fetchall()
        elif user_id is not None:
            items = cursor.execute(
                "SELECT * FROM shared_list_items WHERE family_id IS NULL AND added_by_user_id = ?", (user_id,)
            ).fetchall()
        else:
            raise HTTPException(status_code=400, detail="Missing user_id or family_id")

        return [dict(row) for row in items]

    finally:
        conn.close()



@app.delete("/shared_list_items/{item_id}")
def delete_shared_list_item(item_id: int):
    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM shared_list_items WHERE id = ?", (item_id,))
    conn.commit()
    deleted = cursor.rowcount
    conn.close()

    if deleted == 0:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"message": "Item deleted successfully"}



@app.post("/shared_list_items", status_code=201)
def add_shared_list_item(item: SharedListItem = Body(...)):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        try:
            cursor.execute(
                """
                INSERT INTO shared_list_items (name, family_id, added_by_user_id, timestamp, notes)
                VALUES (?, ?, ?, ?, ?)
                """,
                (item.name, item.family_id, item.added_by_user_id, item.timestamp, item.notes)
            )
            conn.commit()
        except sqlite3.OperationalError as e:
            print("🔒 Database locked:", e)
            raise HTTPException(status_code=500, detail="Database is currently locked. Please try again.")
        

        return {"message": "Shared list item added successfully"}

    finally:
        conn.close()

