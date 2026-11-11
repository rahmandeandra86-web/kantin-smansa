import http.server
import socketserver
import json
import os
import urllib.parse

# Memastikan direktori kerja server selalu sinkron dengan lokasi script
os.chdir(os.path.dirname(os.path.abspath(__file__)))

PORT = int(os.environ.get('PORT', 8080))
DB_FILE = 'database.json'

# Data Default jika database belum ada
DEFAULT_DB = {
    "products": [
        {"id": 1, "category_id": 1, "name": "Nasi Goreng Telur", "price": 12000, "stock": 15, "active": True, "rec": True, "description": "Nasi goreng gurih dengan telur", "cat": "Makanan Berat", "image": "https://images.unsplash.com/photo-1603133872878-684f208fb84b?auto=format&fit=crop&w=300&q=80"},
        {"id": 2, "category_id": 1, "name": "Nasi Ayam Geprek", "price": 15000, "stock": 12, "active": True, "rec": True, "description": "Ayam crispy dengan sambal geprek pedas", "cat": "Makanan Berat", "image": "https://images.unsplash.com/photo-1626509492160-e4fe9e9f3b89?auto=format&fit=crop&w=300&q=80"},
        {"id": 3, "category_id": 1, "name": "Nasi Telur Kecap", "price": 10000, "stock": 20, "active": True, "rec": False, "description": "Nasi putih dengan telur ceplok kecap", "cat": "Makanan Berat", "image": "https://images.unsplash.com/photo-1543339308-43e59d6b73a6?auto=format&fit=crop&w=300&q=80"},
        {"id": 4, "category_id": 1, "name": "Nasi Ayam Suwir", "price": 13000, "stock": 15, "active": True, "rec": False, "description": "Nasi dengan suwiran ayam berbumbu", "cat": "Makanan Berat", "image": "🍽️"},
        {"id": 5, "category_id": 1, "name": "Nasi Uduk", "price": 10000, "stock": 25, "active": True, "rec": False, "description": "Nasi uduk harum khas lengkap", "cat": "Makanan Berat", "image": "🍽️"},
        {"id": 6, "category_id": 2, "name": "Bakwan", "price": 2000, "stock": 30, "active": True, "rec": False, "description": "Bakwan sayur renyah hangat", "cat": "Makanan Ringan", "image": "🥠"},
        {"id": 7, "category_id": 2, "name": "Risoles", "price": 3000, "stock": 25, "active": True, "rec": False, "description": "Risoles isi sayur/ragout", "cat": "Makanan Ringan", "image": "🥟"},
        {"id": 8, "category_id": 2, "name": "Tahu Isi", "price": 2000, "stock": 30, "active": True, "rec": False, "description": "Tahu goreng isi sayuran pedas", "cat": "Makanan Ringan", "image": "🧆"},
        {"id": 9, "category_id": 2, "name": "Cireng", "price": 5000, "stock": 20, "active": True, "rec": False, "description": "Cireng kenyal bumbu rujak", "cat": "Makanan Ringan", "image": "🍘"},
        {"id": 10, "category_id": 2, "name": "Sosis Bakar", "price": 5000, "stock": 15, "active": True, "rec": False, "description": "Sosis panggang saus spesial", "cat": "Makanan Ringan", "image": "🌭"},
        {"id": 11, "category_id": 2, "name": "Kentang Goreng", "price": 7000, "stock": 15, "active": True, "rec": False, "description": "French fries gurih renyah", "cat": "Makanan Ringan", "image": "🍟"},
        {"id": 12, "category_id": 3, "name": "Mie Ayam", "price": 12000, "stock": 15, "active": True, "rec": True, "description": "Mie kenyal topping ayam gurih", "cat": "Mie dan Instan", "image": "🍜"},
        {"id": 13, "category_id": 3, "name": "Seblak", "price": 10000, "stock": 15, "active": True, "rec": False, "description": "Seblak kuah pedas topping lengkap", "cat": "Mie dan Instan", "image": "🍲"},
        {"id": 14, "category_id": 3, "name": "Bakso", "price": 10000, "stock": 20, "active": True, "rec": False, "description": "Bakso sapi kuah kaldu hangat", "cat": "Mie dan Instan", "image": "🥣"},
        {"id": 15, "category_id": 3, "name": "Mie Tek-Tek", "price": 12000, "stock": 15, "active": True, "rec": False, "description": "Mie goreng kuah khas tek-tek", "cat": "Mie dan Instan", "image": "https://images.unsplash.com/photo-1569718212165-3a8278d5f624?auto=format&fit=crop&w=300&q=80"},
        {"id": 16, "category_id": 4, "name": "Es Teh Manis", "price": 3000, "stock": 40, "active": True, "rec": True, "description": "Teh manis dingin menyegarkan", "cat": "Minuman", "image": "https://images.unsplash.com/photo-1556679343-c7306c1976bc?auto=format&fit=crop&w=300&q=80"},
        {"id": 17, "category_id": 4, "name": "Es Cokelat", "price": 5000, "stock": 25, "active": True, "rec": False, "description": "Es cokelat manis pekat", "cat": "Minuman", "image": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?auto=format&fit=crop&w=300&q=80"},
        {"id": 18, "category_id": 4, "name": "Lemon Tea", "price": 5000, "stock": 20, "active": True, "rec": False, "description": "Teh lemon segar asam manis", "cat": "Minuman", "image": "🥤"},
        {"id": 19, "category_id": 4, "name": "Milk Tea", "price": 7000, "stock": 20, "active": True, "rec": False, "description": "Teh susu creamy nikmat", "cat": "Minuman", "image": "🧋"},
        {"id": 20, "category_id": 4, "name": "Es Jeruk", "price": 5000, "stock": 25, "active": True, "rec": False, "description": "Es jeruk peras asli segar", "cat": "Minuman", "image": "🍊"},
        {"id": 21, "category_id": 4, "name": "Air Mineral", "price": 3000, "stock": 50, "active": True, "rec": False, "description": "Air mineral botol 600ml", "cat": "Minuman", "image": "💧"},
        {"id": 22, "category_id": 5, "name": "Pisang Cokelat", "price": 3000, "stock": 20, "active": True, "rec": False, "description": "Piscok lumer renyah", "cat": "Roti & Manis", "image": "🍌"},
        {"id": 23, "category_id": 5, "name": "Roti Bakar", "price": 7000, "stock": 15, "active": True, "rec": False, "description": "Roti bakar selai cokelat keju", "cat": "Roti & Manis", "image": "🍞"},
        {"id": 24, "category_id": 5, "name": "Donat", "price": 3000, "stock": 20, "active": True, "rec": False, "description": "Donat lembut tabur meses", "cat": "Roti & Manis", "image": "🍩"},
        {"id": 25, "category_id": 5, "name": "Puding", "price": 4000, "stock": 15, "active": True, "rec": False, "description": "Puding cokelat lembut", "cat": "Roti & Manis", "image": "🍮"}
    ],
    "categories": [
        {"id": 1, "name": "Makanan Berat"},
        {"id": 2, "name": "Makanan Ringan"},
        {"id": 3, "name": "Mie & Instan"},
        {"id": 4, "name": "Minuman"},
        {"id": 5, "name": "Roti & Manis"}
    ],
    "po": {"status": "open", "label": "Pre-Order Dibuka", "open_time": "07:00", "close_time": "12:00", "mode": "open"},
    "orders": [],
    "vouchers": []
}

def load_db():
    if not os.path.exists(DB_FILE):
        save_db(DEFAULT_DB)
    try:
        with open(DB_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return DEFAULT_DB

def save_db(data):
    with open(DB_FILE, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

class SimpleHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        db = load_db()
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path.rstrip('/')
        query = urllib.parse.parse_qs(parsed_path.query)

        if path == '' or path == '/':
            self.path = '/index.html'
        elif path == '/admin':
            self.path = '/admin.html'
        
        if path == '/api/menu':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            response_data = {
                "categories": db["categories"],
                "products": db["products"],
                "po": db["po"]
            }
            self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))
            return

        elif path in ['/api/admin/orders', '/api/orders']:
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            
            if 'codes' in query:
                codes = query['codes'][0].split(',')
                filtered = [o for o in db['orders'] if o.get('code') in codes]
                self.wfile.write(json.dumps(filtered, ensure_ascii=False).encode('utf-8'))
            else:
                self.wfile.write(json.dumps(db['orders'], ensure_ascii=False).encode('utf-8'))
            return

        elif path == '/api/admin/vouchers':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(db.get('vouchers', []), ensure_ascii=False).encode('utf-8'))
            return

        return super().do_GET()

    def do_POST(self):
        db = load_db()
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path.rstrip('/')
        
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        data = json.loads(body.decode('utf-8')) if body else {}

        if path == '/api/orders':
            import random
            code = 'ORD-' + str(random.randint(100, 999))
            
            total = 0
            processed_items = []
            for item in data.get('items', []):
                p = next((prod for prod in db['products'] if prod['id'] == item['id']), None)
                if p:
                    sub = p['price'] * item['qty']
                    total += sub
                    processed_items.append({"id": p['id'], "name": p['name'], "price": p['price'], "qty": item['qty']})

            new_order = {
                "code": code,
                "name": data.get('name', 'Tanpa Nama'),
                "kelas": data.get('kelas', 'Kelas -'),
                "status": "Menunggu konfirmasi",
                "items": processed_items,
                "total": total,
                "payment": {
                    "method": data.get('payment', 'Tunai'),
                    "status": "Belum bayar" if data.get('payment') == 'Tunai' else "Menunggu verifikasi",
                    "note": data.get('note', '')
                },
                "created": __import__('datetime').datetime.now().isoformat()
            }
            
            db['orders'].insert(0, new_order)
            save_db(db)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True, "code": code}, ensure_ascii=False).encode('utf-8'))
            return

        elif path == '/api/admin/reset':
            db['orders'] = []
            save_db(db)
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}, ensure_ascii=False).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

    def do_PUT(self):
        db = load_db()
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path.rstrip('/')
        
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        data = json.loads(body.decode('utf-8')) if body else {}

        if '/api/admin/orders' in path:
            order_id_or_code = path.split('/')[-1]
            for o in db['orders']:
                if str(o.get('code')) == str(order_id_or_code) or str(o.get('id')) == str(order_id_or_code):
                    if 'status' in data:
                        o['status'] = data['status']
                    if 'payment_status' in data:
                        o['payment']['status'] = data['payment_status']
            save_db(db)
            
            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}, ensure_ascii=False).encode('utf-8'))
            return

        elif path == '/api/admin/po':
            db['po']['open_time'] = data.get('open_time', db['po']['open_time'])
            db['po']['close_time'] = data.get('close_time', db['po']['close_time'])
            db['po']['mode'] = data.get('mode', db['po']['mode'])
            save_db(db)

            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps({"success": True}, ensure_ascii=False).encode('utf-8'))
            return

        self.send_response(404)
        self.end_headers()

if __name__ == '__main__':
    print(f"Server berjalan di port {PORT}...")
    with socketserver.TCPServer(("", PORT), SimpleHandler) as httpd:
        httpd.serve_forever()