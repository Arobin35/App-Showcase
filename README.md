# App-Showcase
# 👨‍🍳 Chef-Pal: Your Digital Kitchen Companion

**Chef-Pal** is an iOS application built with SwiftUI and FastAPI that helps users track their pantry and fridge inventory, avoid food waste, and plan smarter grocery trips—all while supporting shared access for families.

---

## 🎯 Target Audience

- Busy individuals or families who want to stay on top of their groceries
- People who often forget what’s expiring or already bought
- Anyone looking to reduce food waste and save money

---

## ❓ Problem It Solves

Many households face the same recurring problems:
- **Food spoilage** from forgotten items in the fridge or pantry
- **Duplicate purchases** due to unclear inventory
- **Inefficient shopping lists** 

Chef-Pal aims to solve these by:
- Tracking expiration dates of all food items
- Highlighting soon-to-expire items
- Enabling shared access for families (via `familyID`)
- Suggesting recipes based on available ingredients (WIP)
- Offering an organized, visual, and searchable inventory experience

---

## 📲 Core Features

- ✅ **Fridge & Pantry Management**: Add, edit, delete, or update quantities with live API sync
- ✅ **Expiring Soon Section**: Automatically displays top 5 items closest to expiration
- ✅ **Shared Family Lists**: Multiple users with the same family ID can collaborate
- ✅ **Recipe Saving**: Users can save and view recipes (future integration with recommendations)
- ✅ **Search & Sort**: Filter inventory with smart similarity-based search
- ✅ **Deals View**: Placeholder for future grocery deals and discounts
- ✅ **User Profiles**: Personalized accounts with optional profile photos and contact info
- ✅ **Secure Sign-In**: Email/username login with password hash checking

---

## ⚙️ Tech Stack

| Layer         | Technology                 |
|--------------|----------------------------|
| **Frontend** | SwiftUI (iOS 15+), MVVM     |
| **Backend**  | FastAPI (Python 3.11)       |
| **Database** | SQLite (Local persistence)  |
| **API Client** | URLSession + Codable       |
| **Authentication** | Custom login using hashed passwords |
| **Version Control** | Git + GitHub (private repo) |

---

## 🧱 Database Schema (Key Tables)

- `users`: Stores user credentials, profile info, and family IDs
- `food_items` / `pantry_items`: Track quantity, expiration, user ownership
- `families`: Supports grouping users into shared households

📄 See `schema.txt` for full DDL.

---

## 🚧 Development Notes (Learned Swift during the process)
- 🔃 **Agile Workflow**: Iteratively built using Scrum with tasks broken into sprints (e.g., login → item tracking → shared lists)
- 🧪 **Test Users**: Use `UserDefaults` to simulate sessions during development
- 🔍 **Debugging Aids**: Many print statements and response logs are embedded for API tracing
- 🔐 **Local Only**: App currently runs on `localhost:8000` for testing; deploy plan TBD

---

## 🛠 Setup Instructions

1. **Backend**
   - Run `main.py` using `uvicorn main:app --reload`
   - Make sure `pantry.db` is in the root directory

2. **Frontend**
   - Open in Xcode (iOS 15+)
   - Start with `PreviewLauncherView.swift`

3. **Credentials**
   - Use `/users` endpoint to create test users or manually add rows to `users` table

---

## 🚀 Future Enhancements

- 🔄 Real-time syncing across devices
- 🧠 Working AI-generated recipes from available items
- 📱 Push notifications for expiring items
- 🛒 Smart grocery list generation from pantry gaps

---

## 🤝 Credits

Developed by **Abram Robin**  
Designed with love for people who forget what's in their fridge ❤️
