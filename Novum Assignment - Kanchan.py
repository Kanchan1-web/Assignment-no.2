import unittest
import requests

BASE_URL = "https://dummyjson.com/products"

class TestDummyJsonAPI(unittest.TestCase):

    def test_get_single_product(self):
        """✅ Test GET method - To fetch one specific product"""
        product_id = 1  # Sample Product ID
        product_id2 = 500 # Sample Product ID for failed case 1
        product_id3 = "xxx" # Sample Product ID for failed case 2
        product_id4 = "" # Sample Product ID for failed case 3
        response = requests.get(f"{BASE_URL}/{product_id}")
        response2 = requests.get(f"{BASE_URL}/{product_id2}")
        response3 = requests.get(f"{BASE_URL}/{product_id3}")
        response4 = requests.get(f"{BASE_URL}/{product_id4}")
        
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["id"], product_id)
        print(f"GET ✅ | Product ID: {data['id']} | Title: {data['title']}") #Positive test case
        
        self.assertEqual(response2.status_code, 200)
        data2 = response2.json()
        self.assertEqual(data2["id"], product_id2)
        print(f"GET ✅ | Product ID: {data2['id']} | Title: {data2['title']}") #Negative test case 1
        
        response3 = requests.get(f"{BASE_URL}/{product_id3}")
        self.assertEqual(response3.status_code, 200)
        data3 = response3.json()
        self.assertEqual(data3["id"], product_id3)
        print(f"GET ✅ | Product ID: {data3['id']} | Title: {data3['title']}") #Negative test case 2
        
        response4 = requests.get(f"{BASE_URL}/{product_id4}")
        self.assertEqual(response4.status_code, 200)
        data4 = response4.json()
        self.assertEqual(data4["id"], product_id4)
        print(f"GET ✅ | Product ID: {data4['id']} | Title: {data4['title']}") #Negative test case 3

    def test_post_product(self):
        """✅ Test POST method - To add a new product"""
        payload = {
            "title": "Kanchan's iPhone",
            "price": 2499
        } # Positive Test case
        response = requests.post(f"{BASE_URL}/add", json=payload)
        self.assertEqual(response.status_code, 201)
        data = response.json()
        self.assertEqual(data["title"], payload["title"])
        self.product_id = data.get("id")
        print(f"POST ✅ | Product Created ID: {self.product_id}")
        payload2 = {
            "title": "Kanchan's iPhone",
            "price": 2499
        } # Negative Test case 1

    def test_put_product(self):
        """✅ Test PUT method - Update product details"""
        product_id = 1  # Sample Product ID
        payload = {
            "title": "Kanchan's Android Phone",
            "price": 1999
        }
        response = requests.put(f"{BASE_URL}/{product_id}", json=payload)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["price"], payload["price"])
        print(f"PUT ✅ | Product {product_id} Updated")

    def test_delete_product(self):
        """✅ Test DELETE method - Delete a product"""
        product_id = 1  # Sample Product ID
        response = requests.delete(f"{BASE_URL}/{product_id}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data.get("isDeleted", True))
        print(f"DELETE ✅ | Product {product_id} Deleted")
        
    def test_get_all_products(self):
        """✅ Test GET method - To fetch all products"""
        response = requests.get(BASE_URL)
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("products", data)
        print("GET ✅ | Total Products:", data["total"])
     
        
if __name__ == "__main__":
    unittest.main()
