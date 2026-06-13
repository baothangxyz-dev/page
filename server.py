from http.server import HTTPServer, BaseHTTPRequestHandler
import os
import json
from urllib.parse import urlparse, parse_qs

def check_and_create_status_file():
    """Kiểm tra và tạo file status.txt nếu chưa tồn tại"""
    if not os.path.exists("status.txt"):
        with open("status.txt", "w") as f:
            f.write("OFF")

def update_status(new_status):
    """Cập nhật trạng thái vào file"""
    with open("status.txt", "w") as data_base:
        data_base.write(new_status)

def read_current_status():
    """Đọc trạng thái hiện tại từ file"""
    with open("status.txt", "r") as data_base:
        return data_base.read().strip()

class Handler(BaseHTTPRequestHandler):
    
    def do_GET(self):
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        # API endpoint: lấy trạng thái dạng JSON
        if path == '/api/status':
            current_status = read_current_status()
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = json.dumps({'status': current_status})
            self.wfile.write(response.encode())
        
        # API endpoint: bật
        elif path == '/api/status-on':
            update_status('ON')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = json.dumps({'status': 'ON', 'message': 'Đã bật thành công'})
            self.wfile.write(response.encode())
        
        # API endpoint: tắt
        elif path == '/api/status-off':
            update_status('OFF')
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = json.dumps({'status': 'OFF', 'message': 'Đã tắt thành công'})
            self.wfile.write(response.encode())
        
        # Trang chủ - giao diện HTML
        elif path == '/' or path == '/index.html':
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(HTML_PAGE.encode('utf-8'))
        
        # Các route khác - 404
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(b'<h1>404 - Không tìm thấy trang</h1>')
    
    def do_POST(self):
        """Xử lý POST request (nếu cần)"""
        parsed_path = urlparse(self.path)
        path = parsed_path.path
        
        if path == '/api/status':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            
            new_status = data.get('status', '').upper()
            if new_status in ['ON', 'OFF']:
                update_status(new_status)
                self.send_response(200)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps({'status': new_status, 'message': 'Cập nhật thành công'})
                self.wfile.write(response.encode())
            else:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps({'error': 'Status phải là ON hoặc OFF'})
                self.wfile.write(response.encode())
        else:
            self.send_response(404)
            self.end_headers()

# HTML Giao diện tích hợp
HTML_PAGE = '''
<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Điều khiển trạng thái</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: system-ui, -apple-system, 'Segoe UI', Roboto, 'Helvetica Neue', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            color: #fff;
            padding: 20px;
        }

        .card {
            background: rgba(255, 255, 255, 0.95);
            backdrop-filter: blur(10px);
            border-radius: 2rem;
            padding: 2.5rem;
            text-align: center;
            box-shadow: 0 25px 45px rgba(0, 0, 0, 0.2);
            max-width: 500px;
            width: 100%;
            transition: all 0.3s ease;
        }

        h1 {
            font-size: 2rem;
            font-weight: 600;
            margin-bottom: 0.5rem;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            background-clip: text;
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        .subtitle {
            color: #666;
            margin-bottom: 2rem;
            font-size: 0.9rem;
        }

        .status-container {
            background: #f7f7f7;
            border-radius: 1.5rem;
            padding: 2rem;
            margin-bottom: 2rem;
        }

        .status-icon {
            font-size: 6rem;
            margin: 1rem 0;
            display: inline-block;
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        .status-text {
            font-size: 3.5rem;
            font-weight: 800;
            margin: 0.5rem 0;
            text-transform: uppercase;
            letter-spacing: 3px;
        }

        .status-on {
            color: #27ae60;
            text-shadow: 0 0 20px rgba(39, 174, 96, 0.3);
        }

        .status-off {
            color: #e74c3c;
            text-shadow: 0 0 20px rgba(231, 76, 60, 0.3);
        }

        .status-loading {
            color: #95a5a6;
        }

        .btn-group {
            display: flex;
            gap: 1rem;
            justify-content: center;
            margin-bottom: 2rem;
        }

        button {
            flex: 1;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            border: none;
            color: white;
            font-size: 1.1rem;
            font-weight: 600;
            padding: 0.8rem 1.5rem;
            border-radius: 60px;
            cursor: pointer;
            transition: all 0.3s ease;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        }

        button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
        }

        button:active {
            transform: translateY(0);
        }

        .info-panel {
            background: #f0f0f0;
            border-radius: 1rem;
            padding: 1rem;
            margin-top: 1rem;
        }

        .info-item {
            display: flex;
            justify-content: space-between;
            padding: 0.5rem;
            font-size: 0.85rem;
            color: #555;
            border-bottom: 1px solid #ddd;
        }

        .info-item:last-child {
            border-bottom: none;
        }

        .info-label {
            font-weight: 600;
        }

        .info-value {
            font-family: monospace;
            color: #667eea;
        }

        .loading {
            opacity: 0.6;
            pointer-events: none;
        }

        .toast {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: #27ae60;
            color: white;
            padding: 12px 24px;
            border-radius: 8px;
            animation: slideIn 0.3s ease;
            z-index: 1000;
        }

        @keyframes slideIn {
            from {
                transform: translateX(100%);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
    </style>
</head>
<body>
    <div class="card">
        <h1>⚡ Bảng điều khiển</h1>
        <div class="subtitle">Hệ thống quản lý trạng thái</div>
        
        <div class="status-container">
            <div class="status-icon" id="icon">🔄</div>
            <div class="status-text status-loading" id="statusDisplay">Đang tải...</div>
        </div>
        
        <div class="btn-group">
            <button onclick="setStatus('ON')">🟢 BẬT</button>
            <button onclick="setStatus('OFF')">🔴 TẮT</button>
        </div>
        
        <div class="info-panel">
            <div class="info-item">
                <span class="info-label">📁 File lưu trữ:</span>
                <span class="info-value">status.txt</span>
            </div>
            <div class="info-item">
                <span class="info-label">🔄 Trạng thái hiện tại:</span>
                <span class="info-value" id="currentStatusValue">--</span>
            </div>
            <div class="info-item">
                <span class="info-label">🌐 API Server:</span>
                <span class="info-value">localhost:5000</span>
            </div>
        </div>
    </div>

    <script>
        const API_BASE = 'http://localhost:5000';
        
        // Hiển thị thông báo
        function showToast(message, isError = false) {
            const toast = document.createElement('div');
            toast.className = 'toast';
            toast.style.background = isError ? '#e74c3c' : '#27ae60';
            toast.textContent = message;
            document.body.appendChild(toast);
            
            setTimeout(() => {
                toast.remove();
            }, 3000);
        }
        
        // Lấy trạng thái từ server
        async function fetchStatus() {
            try {
                const response = await fetch(`${API_BASE}/api/status`);
                if (!response.ok) throw new Error('Lỗi kết nối');
                const data = await response.json();
                return data.status;
            } catch (error) {
                console.error('Lỗi fetch status:', error);
                showToast('Không thể kết nối đến server!', true);
                return null;
            }
        }
        
        // Cập nhật giao diện
        function updateUI(status) {
            const statusDisplay = document.getElementById('statusDisplay');
            const iconEl = document.getElementById('icon');
            const currentStatusValue = document.getElementById('currentStatusValue');
            
            if (status === 'ON') {
                statusDisplay.innerHTML = 'ON';
                statusDisplay.className = 'status-text status-on';
                iconEl.innerHTML = '🟢';
                currentStatusValue.innerHTML = '<span style="color:#27ae60">● BẬT</span>';
                document.title = 'Trạng thái: BẬT';
            } else if (status === 'OFF') {
                statusDisplay.innerHTML = 'OFF';
                statusDisplay.className = 'status-text status-off';
                iconEl.innerHTML = '🔴';
                currentStatusValue.innerHTML = '<span style="color:#e74c3c">● TẮT</span>';
                document.title = 'Trạng thái: TẮT';
            } else {
                statusDisplay.innerHTML = '?';
                statusDisplay.className = 'status-text';
                iconEl.innerHTML = '⚪';
                currentStatusValue.innerHTML = '--';
            }
        }
        
        // Cập nhật trạng thái (tải từ server)
        async function updateStatusFromServer() {
            const status = await fetchStatus();
            if (status) {
                updateUI(status);
                return status;
            }
            return null;
        }
        
        // Đặt trạng thái mới
        async function setStatus(newStatus) {
            if (newStatus !== 'ON' && newStatus !== 'OFF') return;
            
            // Disable buttons trong lúc xử lý
            const buttons = document.querySelectorAll('button');
            buttons.forEach(btn => btn.disabled = true);
            document.querySelector('.status-text').innerHTML = 'Đang xử lý...';
            
            try {
                const response = await fetch(`${API_BASE}/api/status-${newStatus.toLowerCase()}`);
                if (!response.ok) throw new Error('Lỗi khi cập nhật');
                
                const data = await response.json();
                updateUI(data.status);
                showToast(`✅ ${data.message}`);
                
                // Refresh lại trạng thái để đảm bảo đồng bộ
                await updateStatusFromServer();
            } catch (error) {
                console.error('Lỗi set status:', error);
                showToast('❌ Không thể cập nhật trạng thái!', true);
                // Thử lấy lại trạng thái hiện tại
                await updateStatusFromServer();
            } finally {
                // Enable buttons
                buttons.forEach(btn => btn.disabled = false);
            }
        }
        
        // Tự động cập nhật trạng thái mỗi 5 giây
        let autoRefreshInterval;
        
        function startAutoRefresh() {
            if (autoRefreshInterval) clearInterval(autoRefreshInterval);
            autoRefreshInterval = setInterval(async () => {
                const currentDisplay = document.getElementById('statusDisplay').innerHTML;
                if (currentDisplay !== 'Đang xử lý...') {
                    await updateStatusFromServer();
                }
            }, 5000);
        }
        
        // Khởi tạo khi load trang
        async function init() {
            await updateStatusFromServer();
            startAutoRefresh();
        }
        
        // Cleanup khi rời trang
        window.addEventListener('beforeunload', () => {
            if (autoRefreshInterval) clearInterval(autoRefreshInterval);
        });
        
        init();
    </script>
</body>
</html>
'''

def start_server():
    """Khởi động server"""
    port = 5000
    print(f'🚀 Server đã khởi động!')
    print(f'📱 Truy cập: http://localhost:{port}')
    print(f'📁 File lưu trạng thái: status.txt')
    print(f'🛑 Nhấn Ctrl+C để dừng server')
    print('='*50)
    
    try:
        HTTPServer(('localhost', port), Handler).serve_forever()
    except KeyboardInterrupt:
        print('\n👋 Đang dừng server...')
        print('✅ Server đã dừng!')

# Chạy chương trình
if __name__ == '__main__':
    check_and_create_status_file()
    start_server()
