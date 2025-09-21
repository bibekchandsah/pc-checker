import os
import tempfile
import webbrowser
import threading
import time
from datetime import datetime

class KeyboardTest:
    def __init__(self):
        self.is_testing = False
    
    def run_test(self, callback=None):
        """
        Run keyboard test - opens an interactive HTML page to test all keyboard keys
        """
        results = {
            'test_name': 'Keyboard Test',
            'start_time': datetime.now(),
            'status': 'Running',
            'progress': 0,
            'keyboard_test_url': '',
            'browser_opened': False,
            'instructions_given': False,
            'errors': []
        }
        
        def keyboard_test_worker():
            try:
                # Create a temporary HTML file for keyboard testing
                html_content = self._generate_keyboard_html()
                
                # Create temporary HTML file
                temp_dir = tempfile.gettempdir()
                html_file_path = os.path.join(temp_dir, 'keyboard_test.html')
                
                with open(html_file_path, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                
                results['keyboard_test_url'] = f'file:///{html_file_path.replace(os.sep, "/")}'
                results['progress'] = 25
                
                if callback:
                    callback(results)
                
                # Open the HTML file in default browser
                try:
                    webbrowser.open(html_file_path)
                    results['browser_opened'] = True
                    results['progress'] = 50
                    
                    if callback:
                        callback(results)
                    
                    # Simulate test progression
                    for i in range(5):
                        time.sleep(1)
                        results['progress'] = 50 + (i + 1) * 10
                        if callback:
                            callback(results)
                    
                    results['instructions_given'] = True
                    results['status'] = 'Completed'
                    results['progress'] = 100
                    results['end_time'] = datetime.now()
                    
                    if callback:
                        callback(results)
                        
                except Exception as e:
                    results['errors'].append(f"Failed to open browser: {str(e)}")
                    results['status'] = 'Failed'
                    
            except Exception as e:
                results['errors'].append(f"Keyboard test error: {str(e)}")
                results['status'] = 'Failed'
            
            finally:
                self.is_testing = False
                if callback:
                    callback(results)
        
        # Start the test in a separate thread
        self.is_testing = True
        test_thread = threading.Thread(target=keyboard_test_worker, daemon=True)
        test_thread.start()
        
        return results
    
    def _generate_keyboard_html(self):
        """Generate the HTML content for the keyboard test"""
        return '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎹 Keyboard Test - Test All Your Keys!</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: #333;
            min-height: 100vh;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 20px auto;
            background: #ffffff12;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);
            padding: 30px;
            backdrop-filter: blur(10px);
        }

        .header {
            text-align: center;
            margin-bottom: 30px;
            padding-bottom: 20px;
            border-bottom: 3px solid #e1e8ed;
        }

        .header h1 {
            font-size: 2.5em;
            background: linear-gradient(45deg, #667eea, #764ba2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: #212121;
            margin-bottom: 10px;
        }

        .header p {
            font-size: 1.1em;
            color: #f5eeee;
        }

        .instructions {
            background: #535353d9;
            border-left: 5px solid #667eea;
            padding: 20px;
            margin-bottom: 30px;
            border-radius: 10px;
        }

        .instructions h3 {
            color: #333;
            margin-bottom: 15px;
        }

        .instructions ul {
            list-style-type: none;
        }

        .instructions li {
            margin: 8px 0;
            padding-left: 20px;
            position: relative;
        }

        .instructions li:before {
            content: "✓";
            position: absolute;
            left: 0;
            color: #27ae60;
            font-weight: bold;
        }

        /* Instructions Button */
        .instructions-btn {
            background: #3498db;
            color: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            margin: 20px 0;
            transition: background 0.3s ease;
        }

        .instructions-btn:hover {
            background: #2980b9;
        }

        /* Modal Styles - Glassmorphism */
        .modal {
            display: none;
            position: fixed;
            z-index: 1000;
            left: 0;
            top: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.3);
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            animation: fadeIn 0.4s ease;
        }

        .modal-content {
            background: linear-gradient(135deg, 
                rgba(255, 255, 255, 0.1), 
                rgba(255, 255, 255, 0.05)
            );
            backdrop-filter: blur(20px);
            -webkit-backdrop-filter: blur(20px);
            border: 1px solid rgba(255, 255, 255, 0.2);
            color: #ffffff;
            margin: 2% auto;
            padding: 35px;
            border-radius: 20px;
            width: 90%;
            max-width: 850px;
            max-height: 90vh;
            overflow-y: auto;
            position: relative;
            animation: slideIn 0.4s ease;
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.3),
                inset 0 1px 0 rgba(255, 255, 255, 0.2);
        }

        .modal-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 25px;
            border-bottom: 1px solid rgba(255, 255, 255, 0.2);
            padding-bottom: 20px;
        }

        .modal-title {
            color: #ffffff;
            margin: 0;
            font-size: 26px;
            font-weight: 600;
            text-shadow: 0 2px 10px rgba(0, 0, 0, 0.3);
        }

        .close {
            color: rgba(255, 255, 255, 0.8);
            font-size: 32px;
            font-weight: bold;
            cursor: pointer;
            transition: all 0.3s ease;
            background: rgba(255, 255, 255, 0.1);
            border-radius: 50%;
            width: 45px;
            height: 45px;
            display: flex;
            align-items: center;
            justify-content: center;
            border: 1px solid rgba(255, 255, 255, 0.2);
        }

        .close:hover {
            color: #ffffff;
            background: rgba(231, 76, 60, 0.2);
            border-color: rgba(231, 76, 60, 0.3);
            transform: scale(1.1);
        }

        /* Modal Instructions Styling */
        .modal .instructions {
            color: rgba(255, 255, 255, 0.95);
        }

        .modal .instructions li {
            margin: 12px 0;
            padding-left: 25px;
            line-height: 1.6;
        }

        .modal .instructions li:before {
            content: "✨";
            color: #3498db;
            font-size: 14px;
        }

        .modal .instructions ul ul li:before {
            content: "→";
            color: #52c41a;
        }

        .modal .instructions strong {
            color: #ffffff;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.3);
        }

        .modal .instructions code {
            background: rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.1);
            padding: 2px 6px;
            border-radius: 4px;
            font-family: 'Courier New', monospace;
            color: #e8f4fd;
        }

        .modal .instructions span[style*="color: #f39c12"] {
            color: #f39c12 !important;
            font-weight: bold;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
        }

        .modal .instructions span[style*="color: #27ae60"] {
            color: #27ae60 !important;
            font-weight: bold;
            text-shadow: 0 1px 3px rgba(0, 0, 0, 0.5);
        }

        .modal .instructions span[style*="background"] {
            background: rgba(255, 255, 255, 0.15) !important;
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 3px 8px;
            border-radius: 6px;
            font-weight: 500;
        }

        @keyframes fadeIn {
            from { 
                opacity: 0;
                backdrop-filter: blur(0px);
                -webkit-backdrop-filter: blur(0px);
            }
            to { 
                opacity: 1;
                backdrop-filter: blur(10px);
                -webkit-backdrop-filter: blur(10px);
            }
        }

        @keyframes slideIn {
            from { 
                transform: translateY(-30px) scale(0.95); 
                opacity: 0;
                backdrop-filter: blur(0px);
                -webkit-backdrop-filter: blur(0px);
            }
            to { 
                transform: translateY(0) scale(1); 
                opacity: 1;
                backdrop-filter: blur(20px);
                -webkit-backdrop-filter: blur(20px);
            }
        }

        .keyboard {
            background: #2c3e50;
            padding: 30px;
            border-radius: 15px;
            margin: 30px 0;
            box-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
            width: 100%;
            overflow-x: auto;
        }

        .keyboard-row {
            display: flex;
            justify-content: flex-start;
            margin: 8px 0;
            gap: 6px;
            padding-left: 20px;
        }

        .key {
            background: linear-gradient(145deg, #34495e, #2c3e50);
            border: 2px solid #455a64;
            border-radius: 8px;
            color: #ecf0f1;
            font-family: 'Courier New', monospace;
            font-weight: bold;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s ease;
            min-width: 50px;
            height: 50px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 12px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            position: relative;
            overflow: hidden;
        }

        .key.special {
            background: linear-gradient(145deg, #e74c3c, #c0392b);
            border-color: #e74c3c;
        }

        /* Specific key widths for better alignment */
        .key.escape {
            min-width: 60px;
        }

        .key.backspace {
            min-width: 110px;
        }

        .key.tab {
            min-width: 80px;
        }

        .key.backslash {
            min-width: 80px;
        }

        .key.caps-lock {
            min-width: 100px;
        }

        .key.enter {
            min-width: 115px;
        }

        .key.shift-left {
            min-width: 135px;
        }

        .key.shift-right {
            min-width: 135px;
        }

        .key.ctrl {
            min-width: 83px;
        }

        .key.win {
            min-width: 60px;
        }

        .key.alt {
            min-width: 60px;
        }

        .key.menu {
            min-width: 70px;
        }

        .key.fn {
            min-width: 60px;
        }

        .key.space {
            min-width: 320px;
        }

        /* Navigation and utility keys - standardized size */
        .key.print, .key.scroll-lock, .key.pause, 
        .key.insert, .key.home, .key.page-up, 
        .key.delete, .key.end, .key.page-down, 
        .key.arrow {
            min-width: 60px;
        }

        /* Navigation keys section */
        .nav-section {
            margin-left: 15px;
            display: flex;
            flex-direction: column;
            align-items: flex-start;
            flex: 0 0 auto;
            min-width: 200px;
        }

        .nav-group {
            display: flex;
            flex-direction: column;
            gap: 6px;
        }

        .nav-row {
            display: flex;
            gap: 6px;
            margin: 8px 0 0 0;
        }

        .keyboard-main {
            display: flex;
            align-items: flex-start;
            gap: 15px;
            width: 100%;
            flex-wrap: nowrap;
            min-width: fit-content;
        }

        .main-keyboard {
            flex: 0 0 auto;
        }

        /* Numeric Keypad Section */
        .numpad-section {
            margin-left: 15px;
            display: grid;
            grid-template-columns: repeat(4, 66px);
            grid-template-rows: repeat(5, 54px);
            gap: 6px;
            align-items: start;
            flex: 0 0 auto;
            min-width: 250px;
            margin-top: 65px;
        }

        .numpad-row {
            display: contents; /* This makes grid items position directly in the grid */
        }

        /* Numeric keypad keys - standardized size */
        .key.numpad {
            min-width: 60px;
            height: 48px;
            transition: all 0.3s ease;
        }

        .key.numpad-enter {
            min-width: 60px;
            height: 107px; /* Spans two rows with gap */
            grid-row: span 2;
        }

        .key.numpad-plus {
            min-width: 60px;
            height: 107px; /* Spans two rows with gap */
            grid-row: span 2;
        }

        .key.numpad-zero {
            min-width: 126px; /* Wide zero key spanning two columns */
            height: 48px;
            grid-column: span 2;
        }

        .arrow-section {
            margin-top: 12px;
            display: flex;
            flex-direction: column;
            align-items: center;
        }

        .key.pressed {
            transform: translateY(2px);
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
            background: linear-gradient(145deg, #3498db, #2980b9);
        }

        /* Permanent highlighting classes */
        .key.tested-partial {
            background: linear-gradient(145deg, #f39c12, #e67e22) !important;
            border-color: #f39c12 !important;
            opacity: 0.75;
        }

        .key.tested-complete {
            background: linear-gradient(145deg, #27ae60, #229954) !important;
            border-color: #27ae60 !important;
            opacity: 1.0;
        }

        .key-counter {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: linear-gradient(145deg, #667eea, #764ba2);
            border: 2px solid #667eea;
            border-radius: 12px;
            color: #ffffff;
            font-family: 'Segoe UI', sans-serif;
            font-weight: bold;
            text-align: center;
            min-width: 80px;
            height: 50px;
            margin-left: 15px;
            box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
            position: relative;
            transition: all 0.3s ease;
        }

        #keyCounterNumber {
            font-size: 18px;
            font-weight: 900;
            line-height: 1;
            transition: transform 0.3s ease;
        }

        .counter-label {
            font-size: 9px;
            opacity: 0.9;
            margin-top: 2px;
            line-height: 1;
        }

        /* Zoom animation classes */
        .zoom-in {
            animation: zoomAnimation 0.6s ease;
        }

        @keyframes zoomAnimation {
            0% {
                transform: scale(1);
            }
            50% {
                transform: scale(1.3);
            }
            100% {
                transform: scale(1);
            }
        }

        .progress-bar {
            background: #ecf0f1;
            border-radius: 25px;
            height: 20px;
            margin: 20px 0;
            overflow: hidden;
        }

        .progress-fill {
            background: linear-gradient(45deg, #27ae60, #2ecc71);
            height: 100%;
            border-radius: 25px;
            transition: width 0.3s ease;
            width: 0%;
        }

        @keyframes celebration {
            0%, 100% { transform: scale(1); }
            50% { transform: scale(1.05); }
        }

        #keysPressed {
            background: linear-gradient(135deg, 
                rgba(255, 255, 255, 0.15), 
                rgba(255, 255, 255, 0.08)
            );
            backdrop-filter: blur(15px);
            -webkit-backdrop-filter: blur(15px);
            border: 1px solid rgba(255, 255, 255, 0.25);
            padding: 25px;
            border-radius: 16px;
            margin: 25px 0;
            box-shadow: 
                0 8px 32px rgba(0, 0, 0, 0.1),
                inset 0 1px 0 rgba(255, 255, 255, 0.3);
            transition: all 0.4s ease;
        }

        #keysPressed:hover {
            transform: translateY(-3px);
            background: linear-gradient(135deg, 
                rgba(255, 255, 255, 0.2), 
                rgba(255, 255, 255, 0.1)
            );
            box-shadow: 
                0 12px 40px rgba(0, 0, 0, 0.15),
                inset 0 1px 0 rgba(255, 255, 255, 0.4);
            border-color: rgba(255, 255, 255, 0.35);
        }

        #keysPressed strong {
            color: #ffffff;
            font-size: 18px;
            font-weight: 600;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.3);
        }

        #keyLog {
            color: rgba(255, 255, 255, 0.95);
            font-family: 'Courier New', monospace;
            font-size: 14px;
            line-height: 1.6;
            word-wrap: break-word;
            display: block;
            margin-top: 12px;
            max-height: 120px;
            overflow-y: auto;
            padding: 15px;
            background: linear-gradient(135deg, 
                rgba(0, 0, 0, 0.15), 
                rgba(0, 0, 0, 0.08)
            );
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            border-radius: 10px;
            border: 1px solid rgba(255, 255, 255, 0.15);
            box-shadow: inset 0 2px 10px rgba(0, 0, 0, 0.1);
        }

        /* Custom scrollbar for keyLog */
        #keyLog::-webkit-scrollbar {
            width: 6px;
        }

        #keyLog::-webkit-scrollbar-track {
            background: rgba(255, 255, 255, 0.1);
            border-radius: 3px;
        }

        #keyLog::-webkit-scrollbar-thumb {
            background: rgba(255, 255, 255, 0.3);
            border-radius: 3px;
        }

        #keyLog::-webkit-scrollbar-thumb:hover {
            background: rgba(255, 255, 255, 0.5);
        }

        .footer {
            text-align: center;
            margin-top: 30px;
            padding-top: 20px;
            border-top: 2px solid #e1e8ed;
            color: #666;
        }

        @media (max-width: 768px) {
            .container {
                padding: 15px;
            }
            
            .key {
                min-width: 35px;
                height: 35px;
                font-size: 10px;
            }
            
            /* Mobile-specific key widths */
            .key.escape {
                min-width: 45px;
            }

            .key.backspace {
                min-width: 70px;
            }

            .key.tab {
                min-width: 55px;
            }

            .key.backslash {
                min-width: 55px;
            }

            .key.caps-lock {
                min-width: 65px;
            }

            .key.enter {
                min-width: 75px;
            }

            .key.shift-left {
                min-width: 85px;
            }

            .key.shift-right {
                min-width: 85px;
            }

            .key.ctrl {
                min-width: 50px;
            }

            .key.win {
                min-width: 40px;
            }

            .key.alt {
                min-width: 40px;
            }

            .key.menu {
                min-width: 50px;
            }

            .key.fn {
                min-width: 40px;
            }

            /* Mobile navigation keys */
            .key.print {
                min-width: 45px;
            }

            .key.scroll-lock {
                min-width: 50px;
            }

            .key.pause {
                min-width: 45px;
            }

            .key.insert {
                min-width: 40px;
            }

            .key.home {
                min-width: 45px;
            }

            .key.page-up {
                min-width: 45px;
            }

            .key.delete {
                min-width: 40px;
            }

            .key.end {
                min-width: 40px;
            }

            .key.page-down {
                min-width: 45px;
            }

            .key.arrow {
                min-width: 40px;
            }

            /* Mobile numeric keypad keys */
            .key.numpad {
                min-width: 45px;
            }

            .key.numpad-enter {
                min-width: 45px;
                height: 95px; /* Smaller tall enter for mobile */
            }

            .key.numpad-plus {
                min-width: 45px;
                height: 95px; /* Smaller tall plus for mobile */
            }

            .key.numpad-zero {
                min-width: 96px; /* Smaller wide zero for mobile */
            }

            .nav-section {
                margin-left: 10px;
                min-width: 160px;
            }

            .numpad-section {
                margin-left: 10px;
                min-width: 200px;
                grid-template-columns: repeat(4, 50px);
                grid-template-rows: repeat(5, 45px);
                gap: 4px;
            }

            .keyboard-main {
                flex-direction: row;
                gap: 10px;
                overflow-x: auto;
            }
            
            .key.space {
                min-width: 180px;
            }
            
            .stats {
                flex-direction: column;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎹 Keyboard Test</h1>
            <p>Test all your keyboard keys to ensure they're working properly!</p>
            <button class="instructions-btn" onclick="openModal()">📋 View Instructions</button>
        </div>

        <div id="keysPressed">
            <strong>Keys Pressed:</strong> <span id="keyLog">None yet - start pressing keys!</span>
        </div>

        <div class="keyboard">
            <div class="keyboard-main">
                <div class="main-keyboard">
                    <!-- Function Keys Row -->
                    <div class="keyboard-row">
                        <div class="key escape" data-key="Escape">Esc</div>
                        <div class="key" data-key="F1">F1</div>
                        <div class="key" data-key="F2">F2</div>
                        <div class="key" data-key="F3">F3</div>
                        <div class="key" data-key="F4">F4</div>
                        <div class="key" data-key="F5">F5</div>
                        <div class="key" data-key="F6">F6</div>
                        <div class="key" data-key="F7">F7</div>
                        <div class="key" data-key="F8">F8</div>
                        <div class="key" data-key="F9">F9</div>
                        <div class="key" data-key="F10">F10</div>
                        <div class="key" data-key="F11">F11</div>
                        <div class="key" data-key="F12">F12</div>
                        <div class="key-counter">
                            <span id="keyCounterNumber">0</span>
                            <span class="counter-label">Keys Tested</span>
                        </div>
                    </div>

                    <!-- Number Row -->
                    <div class="keyboard-row">
                        <div class="key" data-key="`">~<br>`</div>
                        <div class="key" data-key="1">!<br>1</div>
                        <div class="key" data-key="2">@<br>2</div>
                        <div class="key" data-key="3">#<br>3</div>
                        <div class="key" data-key="4">$<br>4</div>
                        <div class="key" data-key="5">%<br>5</div>
                        <div class="key" data-key="6">^<br>6</div>
                        <div class="key" data-key="7">&<br>7</div>
                        <div class="key" data-key="8">*<br>8</div>
                        <div class="key" data-key="9">(<br>9</div>
                        <div class="key" data-key="0">)<br>0</div>
                        <div class="key" data-key="-">_<br>-</div>
                        <div class="key" data-key="=">+<br>=</div>
                        <div class="key special backspace" data-key="Backspace">Backspace</div>
                    </div>

                    <!-- QWERTY Top Row -->
                    <div class="keyboard-row">
                        <div class="key special tab" data-key="Tab">Tab</div>
                        <div class="key" data-key="q">Q</div>
                        <div class="key" data-key="w">W</div>
                        <div class="key" data-key="e">E</div>
                        <div class="key" data-key="r">R</div>
                        <div class="key" data-key="t">T</div>
                        <div class="key" data-key="y">Y</div>
                        <div class="key" data-key="u">U</div>
                        <div class="key" data-key="i">I</div>
                        <div class="key" data-key="o">O</div>
                        <div class="key" data-key="p">P</div>
                        <div class="key" data-key="[">{<br>[</div>
                        <div class="key" data-key="]">}<br>]</div>
                        <div class="key special backslash" data-key="backslash">|<br>\\</div>
                    </div>

                    <!-- ASDF Home Row -->
                    <div class="keyboard-row">
                        <div class="key special caps-lock" data-key="CapsLock">Caps Lock</div>
                        <div class="key" data-key="a">A</div>
                        <div class="key" data-key="s">S</div>
                        <div class="key" data-key="d">D</div>
                        <div class="key" data-key="f">F</div>
                        <div class="key" data-key="g">G</div>
                        <div class="key" data-key="h">H</div>
                        <div class="key" data-key="j">J</div>
                        <div class="key" data-key="k">K</div>
                        <div class="key" data-key="l">L</div>
                        <div class="key" data-key="semicolon">:<br>;</div>
                        <div class="key" data-key="quote">"<br>'</div>
                        <div class="key special enter" data-key="Enter">Enter</div>
                    </div>

                    <!-- ZXCV Bottom Row -->
                    <div class="keyboard-row">
                        <div class="key special shift-left" data-key="ShiftLeft">Shift</div>
                        <div class="key" data-key="z">Z</div>
                        <div class="key" data-key="x">X</div>
                        <div class="key" data-key="c">C</div>
                        <div class="key" data-key="v">V</div>
                        <div class="key" data-key="b">B</div>
                        <div class="key" data-key="n">N</div>
                        <div class="key" data-key="m">M</div>
                        <div class="key" data-key=","><br>,</div>
                        <div class="key" data-key=".">><br>.</div>
                        <div class="key" data-key="/">?<br>/</div>
                        <div class="key special shift-right" data-key="ShiftRight">Shift</div>
                    </div>

                    <!-- Space Row -->
                    <div class="keyboard-row">
                        <div class="key special ctrl" data-key="ControlLeft">Ctrl</div>
                        <div class="key special win" data-key="MetaLeft">Win</div>
                        <div class="key special alt" data-key="AltLeft">Alt</div>
                        <div class="key space" data-key=" ">Space</div>
                        <div class="key special alt" data-key="AltRight">Alt</div>
                        <div class="key special fn" data-key="Fn">Fn</div>
                        <div class="key special menu" data-key="ContextMenu">Menu</div>
                        <div class="key special ctrl" data-key="ControlRight">Ctrl</div>
                    </div>
                </div>

                <!-- Navigation Keys Section -->
                <div class="nav-section">
                    <!-- System Keys Row (Print/Scroll/Pause) aligned with Function keys -->
                    <div class="nav-row">
                        <div class="key special print" data-key="PrintScreen">Print</div>
                        <div class="key special scroll-lock" data-key="ScrollLock">Scroll</div>
                        <div class="key special pause" data-key="Pause">Pause</div>
                    </div>

                    <!-- Insert/Home/PageUp Row aligned with Number row -->
                    <div class="nav-row">
                        <div class="key special insert" data-key="Insert">Ins</div>
                        <div class="key special home" data-key="Home">Home</div>
                        <div class="key special page-up" data-key="PageUp">PgUp</div>
                    </div>

                    <!-- Delete/End/PageDown Row aligned with QWERTY row -->
                    <div class="nav-row">
                        <div class="key special delete" data-key="Delete">Del</div>
                        <div class="key special end" data-key="End">End</div>
                        <div class="key special page-down" data-key="PageDown">PgDn</div>
                    </div>

                    <!-- Empty space to align with home row -->
                    <!-- <div style="height: 53px;"></div> -->

                    <!-- Empty space to align with shift row -->
                    <div style="height: 46px;"></div>

                    <!-- Arrow Keys Section aligned with space row -->
                    <div class="arrow-section">
                        <!-- Up Arrow -->
                        <div class="nav-row">
                            <div style="width: 56px;"></div>
                            <div class="key special arrow" data-key="ArrowUp">↑</div>
                            <div style="width: 56px;"></div>
                        </div>
                        <!-- Left/Down/Right Arrows -->
                        <div class="nav-row">
                            <div class="key special arrow" data-key="ArrowLeft">←</div>
                            <div class="key special arrow" data-key="ArrowDown">↓</div>
                            <div class="key special arrow" data-key="ArrowRight">→</div>
                        </div>
                    </div>
                </div>

                <!-- Numeric Keypad Section -->
                <div class="numpad-section">
                    <!-- Row 1: Num Lock / * - -->
                    <div class="key special numpad" data-key="NumLock">Num</div>
                    <div class="key numpad" data-key="NumpadDivide">/</div>
                    <div class="key numpad" data-key="NumpadMultiply">*</div>
                    <div class="key numpad" data-key="NumpadSubtract">-</div>
                    
                    <!-- Row 2: 7 8 9 + (tall) -->
                    <div class="key numpad" data-key="Numpad7">7</div>
                    <div class="key numpad" data-key="Numpad8">8</div>
                    <div class="key numpad" data-key="Numpad9">9</div>
                    <div class="key numpad numpad-plus" data-key="NumpadAdd">+</div>
                    
                    <!-- Row 3: 4 5 6 (+ continues) -->
                    <div class="key numpad" data-key="Numpad4">4</div>
                    <div class="key numpad" data-key="Numpad5">5</div>
                    <div class="key numpad" data-key="Numpad6">6</div>
                    <!-- Plus key spans from above -->
                    
                    <!-- Row 4: 1 2 3 Enter (tall) -->
                    <div class="key numpad" data-key="Numpad1">1</div>
                    <div class="key numpad" data-key="Numpad2">2</div>
                    <div class="key numpad" data-key="Numpad3">3</div>
                    <div class="key numpad numpad-enter" data-key="NumpadEnter">Enter</div>
                    
                    <!-- Row 5: 0 (wide) . (Enter continues) -->
                    <div class="key numpad numpad-zero" data-key="Numpad0">0</div>
                    <div class="key numpad" data-key="NumpadDecimal">.</div>
                    <!-- Enter key spans from above -->
                </div>
            </div>
        </div>
    </div>

    <!-- Instructions Modal -->
    <div id="instructionsModal" class="modal">
        <div class="modal-content">
            <div class="modal-header">
                <h2 class="modal-title">📋 Keyboard Test Instructions</h2>
                <span class="close" onclick="closeModal()">&times;</span>
            </div>
            <div class="instructions">
                <ul>
                    <li>Press any key on your keyboard to test it</li>
                    <li><strong>Visual Feedback System:</strong></li>
                    <ul>
                        <li><span style="color: #f39c12; font-weight: bold;">ORANGE (75% opacity)</span> = First variant tested</li>
                        <li><span style="color: #27ae60; font-weight: bold;">GREEN (100% opacity)</span> = Both variants tested (complete)</li>
                        <li>Keys stay highlighted permanently to show your progress</li>
                    </ul>
                    <li><strong>Dual-variant keys require both presses:</strong></li>
                    <ul>
                        <li><strong>Numbers:</strong> <code>1234567890</code> → <code>!@#$%^&*()</code></li>
                        <li><strong>Symbols:</strong> <code>-=[]\\;',./`</code> → <code>_+{}|:"<>?~</code></li>
                        <li>Press regular key = <span style="color: #f39c12;">Orange</span>, then Shift+key = <span style="color: #27ae60;">Green</span></li>
                    </ul>
                    <li><strong>Single-variant keys go directly to green:</strong></li>
                    <ul>
                        <li>Letters (A-Z), Function keys (F1-F12), Special keys (Ctrl, Alt, Space, etc.)</li>
                    </ul>
                    <li><strong>Example progression:</strong></li>
                    <ul>
                        <li>Press <code>1</code> → Key turns <span style="color: #f39c12;">Orange</span></li>
                        <li>Press <code>Shift+1 (!)</code> → Key turns <span style="color: #27ae60;">Green</span></li>
                    </ul>
                    <li><strong>Numeric Keypad:</strong> All keypad keys (numbers and operators) are always active</li>
                    <li>Aim for all dual-variant keys to turn <span style="color: #27ae60; font-weight: bold;">GREEN</span> for complete testing</li>
                </ul>
            </div>
        </div>
    </div>

    <script>
        let testedKeys = new Set();
        let previousKeyCount = 0;
        let testedKeyElements = new Map(); // Track which physical keys have been tested
        let totalKeys = 180; // Increased to include navigation keys and numeric keypad
        let keyLog = [];

        // Modal functions
        function openModal() {
            document.getElementById('instructionsModal').style.display = 'block';
        }

        function closeModal() {
            document.getElementById('instructionsModal').style.display = 'none';
        }

        // Close modal when clicking outside of it
        window.onclick = function(event) {
            const modal = document.getElementById('instructionsModal');
            if (event.target === modal) {
                closeModal();
            }
        }

        // Keys that have both regular and shift variants (numbers and symbols only)
        let dualKeys = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 
                       '[', ']', '\\\\', ';', "'", ',', '.', '/', '`'];

        document.addEventListener('keydown', function(event) {
            event.preventDefault();
            
            let keyCode = event.code || event.key;
            let keyDisplay = event.key;
            let keyElement = null;
            let baseKey = null;
            
            // Handle Num Lock key
            if (event.code === 'NumLock') {
                keyCode = 'NumLock';
                keyDisplay = 'Num Lock';
                baseKey = 'NumLock';
            }
            // Handle all numpad keys - always active regardless of Num Lock state
            else if (event.code.startsWith('Numpad') && event.code !== 'NumLock') {
                keyCode = event.code;
                keyDisplay = event.key;
                baseKey = event.code;
            }
            // Special key mappings for modifier keys
            else if (event.code === 'ShiftLeft' || event.code === 'ShiftRight') {
                keyCode = event.code;
                keyDisplay = 'Shift';
                baseKey = keyCode;
            } else if (event.code === 'ControlLeft' || event.code === 'ControlRight') {
                keyCode = event.code;
                keyDisplay = 'Ctrl';
                baseKey = keyCode;
            } else if (event.code === 'AltLeft' || event.code === 'AltRight') {
                keyCode = event.code;
                keyDisplay = 'Alt';
                baseKey = keyCode;
            } else if (event.code === 'MetaLeft' || event.code === 'MetaRight') {
                keyCode = event.code;
                keyDisplay = 'Win';
                baseKey = keyCode;
            } else if (event.code === 'Fn' || event.key === 'Fn') {
                keyCode = 'Fn';
                keyDisplay = 'Fn';
                baseKey = 'Fn';
            }
            
            // Special handling for symbol keys (Shift + number/symbol combinations)
            // Map symbols to their base keys for highlighting
            let symbolMap = {
                '!': '1', '@': '2', '#': '3', '$': '4', '%': '5',
                '^': '6', '&': '7', '*': '8', '(': '9', ')': '0',
                '_': '-', '+': '=', '|': '\\\\', '{': '[', '}': ']',
                ':': ';', '"': "'", '<': ',', '>': '.', '?': '/',
                '~': '`'
            };
            
            // Find the corresponding key element (with protection for special characters)
            try {
                keyElement = document.querySelector(`[data-key="${keyCode}"]`);
            } catch(e) {
                // keyCode contains special characters that break querySelector
                keyElement = null;
            }
            
            if (!keyElement) {
                try {
                    keyElement = document.querySelector(`[data-key="${event.key}"]`);
                } catch(e) {
                    // event.key contains special characters that break querySelector
                    keyElement = null;
                }
            }
            
            if (!keyElement) {
                try {
                    keyElement = document.querySelector(`[data-key="${event.key.toLowerCase()}"]`);
                } catch(e) {
                    // event.key.toLowerCase() contains special characters that break querySelector
                    keyElement = null;
                }
            }
            
            // Check if this is a symbol key press (Shift + key that produces a symbol)
            let isSymbolKey = false;
            if (symbolMap[event.key]) {
                // This is a symbol like !, @, #, etc.
                baseKey = symbolMap[event.key]; // Get the base key (1, 2, 3, etc.)
                if (!keyElement) {
                    keyElement = document.querySelector(`[data-key="${baseKey}"]`);
                }
                isSymbolKey = true;
            } else if (dualKeys.includes(event.key)) {
                // This is a regular dual key like 1, 2, 3, -, =, etc.
                baseKey = event.key;
                isSymbolKey = false;
            }
            
            // Special cases for other keys
            if (!keyElement) {
                if (event.key === ' ') {
                    keyElement = document.querySelector('[data-key=" "]');
                    keyCode = ' ';
                    baseKey = ' ';
                } else if (event.key === 'Enter') {
                    keyElement = document.querySelector('[data-key="Enter"]');
                    keyCode = 'Enter';
                    baseKey = 'Enter';
                } else if (event.key === 'Tab') {
                    keyElement = document.querySelector('[data-key="Tab"]');
                    keyCode = 'Tab';
                    baseKey = 'Tab';
                } else if (event.key === 'Backspace') {
                    keyElement = document.querySelector('[data-key="Backspace"]');
                    keyCode = 'Backspace';
                    baseKey = 'Backspace';
                } else if (event.key === 'Escape') {
                    keyElement = document.querySelector('[data-key="Escape"]');
                    keyCode = 'Escape';
                    baseKey = 'Escape';
                } else if (event.key === 'CapsLock') {
                    keyElement = document.querySelector('[data-key="CapsLock"]');
                    keyCode = 'CapsLock';
                    baseKey = 'CapsLock';
                } else if (event.key === ';' || event.key === ':') {
                    keyElement = document.querySelector('[data-key="semicolon"]');
                    keyCode = ';';
                    baseKey = ';';
                } else if (event.key === "'" || event.key === '"') {
                    keyElement = document.querySelector('[data-key="quote"]');
                    keyCode = "'";
                    baseKey = "'";
                } else if (event.key === '\\\\' || event.key === '|') {
                    keyElement = document.querySelector('[data-key="backslash"]');
                    keyCode = '\\\\';
                    baseKey = '\\\\';
                } else if (event.key === 'PrintScreen' || event.code === 'PrintScreen') {
                    keyElement = document.querySelector('[data-key="PrintScreen"]');
                    keyCode = 'PrintScreen';
                    baseKey = 'PrintScreen';
                } else if (event.key === 'ScrollLock') {
                    keyElement = document.querySelector('[data-key="ScrollLock"]');
                    keyCode = 'ScrollLock';
                    baseKey = 'ScrollLock';
                } else if (event.key === 'Pause') {
                    keyElement = document.querySelector('[data-key="Pause"]');
                    keyCode = 'Pause';
                    baseKey = 'Pause';
                } else if (event.key === 'Insert') {
                    keyElement = document.querySelector('[data-key="Insert"]');
                    keyCode = 'Insert';
                    baseKey = 'Insert';
                } else if (event.key === 'Home') {
                    keyElement = document.querySelector('[data-key="Home"]');
                    keyCode = 'Home';
                    baseKey = 'Home';
                } else if (event.key === 'PageUp') {
                    keyElement = document.querySelector('[data-key="PageUp"]');
                    keyCode = 'PageUp';
                    baseKey = 'PageUp';
                } else if (event.key === 'Delete') {
                    keyElement = document.querySelector('[data-key="Delete"]');
                    keyCode = 'Delete';
                    baseKey = 'Delete';
                } else if (event.key === 'End') {
                    keyElement = document.querySelector('[data-key="End"]');
                    keyCode = 'End';
                    baseKey = 'End';
                } else if (event.key === 'PageDown') {
                    keyElement = document.querySelector('[data-key="PageDown"]');
                    keyCode = 'PageDown';
                    baseKey = 'PageDown';
                } else if (event.key === 'ArrowUp') {
                    keyElement = document.querySelector('[data-key="ArrowUp"]');
                    keyCode = 'ArrowUp';
                    baseKey = 'ArrowUp';
                } else if (event.key === 'ArrowDown') {
                    keyElement = document.querySelector('[data-key="ArrowDown"]');
                    keyCode = 'ArrowDown';
                    baseKey = 'ArrowDown';
                } else if (event.key === 'ArrowLeft') {
                    keyElement = document.querySelector('[data-key="ArrowLeft"]');
                    keyCode = 'ArrowLeft';
                    baseKey = 'ArrowLeft';
                } else if (event.key === 'ArrowRight') {
                    keyElement = document.querySelector('[data-key="ArrowRight"]');
                    keyCode = 'ArrowRight';
                    baseKey = 'ArrowRight';
                }
            }
            
            // Handle function keys F1-F12
            if (!keyElement && event.key.match(/^F([1-9]|1[0-2])$/)) {
                keyElement = document.querySelector(`[data-key="${event.key}"]`);
                keyCode = event.key;
                baseKey = event.key;
            }
            
            // Fallback: try to find element using event.code if event.key didn't work
            if (!keyElement && event.code) {
                keyElement = document.querySelector(`[data-key="${event.code}"]`);
                if (keyElement) {
                    keyCode = event.code;
                    baseKey = event.code;
                }
            }
            
            // Additional fallback for letter keys
            if (!keyElement && event.key.length === 1 && event.key.match(/[a-zA-Z]/)) {
                baseKey = event.key.toLowerCase();
                keyElement = document.querySelector(`[data-key="${baseKey}"]`);
                keyCode = baseKey;
            }
            
            // Set baseKey if not already set
            if (!baseKey) {
                baseKey = keyCode;
            }
            
            if (keyElement) {
                // Add temporary pressed effect
                keyElement.classList.add('pressed');
                
                // Use a combination of the actual key pressed and base key for unique tracking
                let trackingKey = keyCode + (event.shiftKey ? '_shift' : '');
                testedKeys.add(trackingKey);
                
                // Track the physical key element and its variants
                if (!testedKeyElements.has(baseKey)) {
                    testedKeyElements.set(baseKey, { regular: false, shift: false });
                }
                
                // Update the tracking for this physical key
                let keyTracking = testedKeyElements.get(baseKey);
                
                // Check if this is a symbol key (pressed with Shift or mapped symbol)
                if (event.shiftKey || isSymbolKey) {
                    keyTracking.shift = true;
                } else {
                    keyTracking.regular = true;
                }
                
                // Apply permanent highlighting based on completion status
                updateKeyHighlighting(keyElement, baseKey, keyTracking);
                
                // Add to key log
                keyLog.push(keyDisplay);
                // Show all keys - no limit
                
                updateStats();
                
                // Remove pressed class after animation
                setTimeout(() => {
                    keyElement.classList.remove('pressed');
                }, 300);
            }
        });

        function updateKeyHighlighting(keyElement, baseKey, keyTracking) {
            // Remove existing permanent classes
            keyElement.classList.remove('tested-partial', 'tested-complete');
            
            // Check if this key has both regular and shift variants (only numbers and symbols)
            let isDualKey = dualKeys.includes(baseKey);
            
            // Numpad keys should always be treated as single keys
            let isNumpadKey = baseKey.startsWith('Numpad') || keyElement.classList.contains('numpad');
            
            if (isDualKey && !isNumpadKey) {
                // For dual keys (numbers/symbols), check if both variants are tested
                if (keyTracking.regular && keyTracking.shift) {
                    // Both variants tested - full opacity (100%)
                    keyElement.classList.add('tested-complete');
                } else if (keyTracking.regular || keyTracking.shift) {
                    // Only one variant tested - partial opacity (75%)
                    keyElement.classList.add('tested-partial');
                }
            } else {
                // For single keys (letters, function keys, numpad keys, etc.), mark as complete when tested
                if (keyTracking.regular || keyTracking.shift) {
                    keyElement.classList.add('tested-complete');
                }
            }
        }

        function updateStats() {
            const keysTestedCount = testedKeys.size;
            
            // Update the counter beside F12 with animation
            const counterElement = document.getElementById('keyCounterNumber');
            if (counterElement) {
                // Only animate if the count has increased
                if (keysTestedCount > previousKeyCount) {
                    // Remove any existing animation class
                    counterElement.classList.remove('zoom-in');
                    
                    // Update the number
                    counterElement.textContent = keysTestedCount;
                    
                    // Trigger animation by adding the class
                    void counterElement.offsetWidth; // Force reflow
                    counterElement.classList.add('zoom-in');
                    
                    // Remove animation class after animation completes
                    setTimeout(() => {
                        counterElement.classList.remove('zoom-in');
                    }, 600);
                } else {
                    // Just update the number without animation
                    counterElement.textContent = keysTestedCount;
                }
            }
            
            // Update previous count for next comparison
            previousKeyCount = keysTestedCount;
            
            document.getElementById('keyLog').textContent = keyLog.join(', ') || 'None yet - start pressing keys!';
        }
        
        // Initial stats update
        updateStats();
    </script>
</body>
</html>
                '''