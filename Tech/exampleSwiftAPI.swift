 // ------------------ FETCH FRIDGE ITEMS (With userID) ------------------ //
    func fetchFridgeItems(userID: String, completion: @escaping ([FoodItem]?, Error?) -> Void) {
        let encodedUserID = userID.addingPercentEncoding(withAllowedCharacters: .urlPathAllowed) ?? ""
        let urlString = "http://127.0.0.1:8000/food_items/\(encodedUserID)"

        guard let url = URL(string: urlString) else {
            print("❌ Invalid URL: \(urlString)")
            completion(nil, NSError(domain: "Invalid URL", code: 400, userInfo: nil))
            return
        }

        print("📡 Sending GET request to: \(urlString)")

        URLSession.shared.dataTask(with: url) { data, response, error in
            if let error = error {
                print("❌ Network error: \(error.localizedDescription)")
                completion(nil, error)
                return
            }

            if let httpResponse = response as? HTTPURLResponse {
                print("📡 Response Status Code: \(httpResponse.statusCode)")
            }

            guard let data = data else {
                print("❌ No data received from backend")
                completion(nil, NSError(domain: "No Data", code: 500, userInfo: nil))
                return
            }

            if let jsonString = String(data: data, encoding: .utf8) {
                print("📡 API Response: \(jsonString)")
            }

            do {
                let response = try JSONDecoder().decode(FoodItemsResponse.self, from: data)
                print("✅ Successfully fetched \(response.food_items.count) food items")
                completion(response.food_items, nil)
            } catch {
                print("❌ JSON Decoding error: \(error.localizedDescription)")
                completion(nil, error)
            }
        }.resume()
    }
    
    
    
    
    func addFridgeItem(_ item: FoodItem, completion: @escaping (Error?) -> Void) {
        let urlString = "http://127.0.0.1:8000/food_items"

        guard let url = URL(string: urlString) else {
            completion(NSError(domain: "", code: 400, userInfo: [NSLocalizedDescriptionKey: "Invalid URL"]))
            return
        }

        var request = URLRequest(url: url)
        request.httpMethod = "POST"
        request.addValue("application/json", forHTTPHeaderField: "Content-Type")

        guard let userIDInt = Int(UserDefaults.standard.string(forKey: "loggedInUserID") ?? "0") else {
            print("❌ Error: User ID is not valid")
            completion(NSError(domain: "", code: 400, userInfo: [NSLocalizedDescriptionKey: "User ID invalid"]))
            return
        }

        var newItem = item
        newItem.user_id = userIDInt

        let body: [String: Any] = [
            "name": newItem.name,
            "quantity": newItem.quantity,
            "expiration_date": newItem.expiration_date,
            "user_id": String(userIDInt)
        ]

        do {
            let jsonData = try JSONSerialization.data(withJSONObject: body)

            if let jsonString = String(data: jsonData, encoding: .utf8) {
                print("📡 Sending POST request to \(urlString) with JSON payload: \(jsonString)")
            }

            request.httpBody = jsonData
        } catch {
            completion(error)
            return
        }

        URLSession.shared.dataTask(with: request) { _, response, error in
            if let error = error {
                print("❌ Failed to add item: \(error.localizedDescription)")
                completion(error)
                return
            }

            if let httpResponse = response as? HTTPURLResponse {
                print("📡 Server response status: \(httpResponse.statusCode)")
                if httpResponse.statusCode != 201 {
                    completion(NSError(domain: "Server Error", code: httpResponse.statusCode, userInfo: nil))
                } else {
                    print("✅ Successfully added item!")
                    completion(nil)
                }
            }
        }.resume()
    }
