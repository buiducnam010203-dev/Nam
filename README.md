<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <title>HEADLOCK VER2</title>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0-beta3/css/all.min.css">
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
        }

        body {
            background-color: #0b0b0b;
            color: white;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            overflow: hidden;
        }

        .phone-frame {
            width: 100%;
            max-width: 414px;
            height: 100vh;
            max-height: 896px;
            background-color: black;
            position: relative;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }

        .status-bar {
            display: flex;
            justify-content: space-between;
            padding: 12px 25px;
            font-size: 14px;
            font-weight: 600;
            color: #fff;
            width: 100%;
            z-index: 10;
        }

        .status-bar .icons {
            display: flex;
            gap: 6px;
        }

        .app-screen {
            padding: 10px 20px 80px 20px;
            flex: 1;
            overflow-y: auto;
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 16px;
        }

        .app-header {
            width: 100%;
            display: flex;
            justify-content: space-between;
            align-items: center;
            color: #fff;
        }

        .back-icon {
            font-size: 0.95rem;
            color: #bbb;
            display: flex;
            align-items: center;
            gap: 6px;
        }

        .header-title {
            text-align: center;
            flex-grow: 1;
            font-weight: 700;
            font-size: 1.05rem;
            letter-spacing: 0.5px;
        }

        .header-title span.sub-title {
            display: block;
            font-size: 0.75rem;
            font-weight: 400;
            color: #888;
        }

        .server-status-wrap {
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.75rem;
            color: #00e676;
            gap: 5px;
            margin-bottom: 2px;
        }

        .server-dot {
            width: 6px;
            height: 6px;
            background-color: #00e676;
            border-radius: 50%;
            box-shadow: 0 0 8px #00e676;
        }

        .menu-icon {
            font-size: 1.2rem;
            color: #fff;
        }

        .avatar-container {
            position: relative;
            margin-top: 10px;
            margin-bottom: 5px;
        }

        .avatar {
            width: 85px;
            height: 85px;
            border-radius: 50%;
            border: 3px solid #222;
            object-fit: cover;
        }

        .badge {
            position: absolute;
            bottom: 2px;
            right: 2px;
            background-color: #1e1e1e;
            border: 2px solid #000;
            border-radius: 50%;
            width: 26px;
            height: 26px;
            display: flex;
            justify-content: center;
            align-items: center;
            font-size: 0.75rem;
            color: #aaa;
        }

        .controls-panel {
            width: 100%;
            background-color: #161618;
            border-radius: 24px;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 20px;
            border: 1px solid #26262a;
        }

        .control-item {
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .control-label {
            display: flex;
            align-items: center;
            font-size: 0.95rem;
            font-weight: 600;
            color: #f1f1f1;
            letter-spacing: 0.3px;
        }

        .control-label i {
            margin-right: 14px;
            width: 20px;
            text-align: center;
            font-size: 1.1rem;
        }

        .switch {
            position: relative;
            display: inline-block;
            width: 48px;
            height: 26px;
        }

        .switch input { 
            opacity: 0;
            width: 0;
            height: 0;
        }

        .slider {
            position: absolute;
            cursor: pointer;
            top: 0; left: 0; right: 0; bottom: 0;
            background-color: #333;
            transition: .3s;
            border-radius: 34px;
        }

        .slider:before {
            position: absolute;
            content: "";
            height: 20px;
            width: 20px;
            left: 3px;
            bottom: 3px;
            background-color: white;
            transition: .3s;
            border-radius: 50%;
        }

        input:checked + .slider {
            background-color: #ffffff;
        }

        input:checked + .slider:before {
            transform: translateX(22px);
            background-color: #000;
        }

        .import-card {
            width: 100%;
            background-color: #161618;
            border-radius: 20px;
            padding: 16px;
            text-align: center;
            border: 1px solid #26262a;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }

        .import-title {
            font-size: 0.75rem;
            letter-spacing: 1.5px;
            color: #777;
            font-weight: 700;
        }

        .import-btn {
            width: 100%;
            padding: 12px;
            background: linear-gradient(90deg, #2563eb, #3b82f6);
            color: white;
            border: none;
            border-radius: 12px;
            font-size: 0.95rem;
            font-weight: 600;
            cursor: pointer;
            box-shadow: 0 4px 12px rgba(37, 99, 235, 0.3);
        }

        .import-sub {
            color: #666;
            font-size: 0.75rem;
        }

        .toolbar {
            position: absolute;
            bottom: 0;
            left: 0;
            width: 100%;
            padding: 12px 16px 24px 16px;
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            background: linear-gradient(to top, rgba(0,0,0,0.95) 60%, transparent);
            z-index: 20;
        }

        .comment-box {
            width: 68%;
            background-color: rgba(255, 255, 255, 0.08);
            border-radius: 16px;
            padding: 10px 14px;
            color: #ddd;
            font-size: 0.85rem;
            backdrop-filter: blur(10px);
        }

        .user-info {
            font-weight: 700;
            margin-bottom: 3px;
            color: #fff;
        }

        .user-info span {
            color: #888;
            font-weight: 400;
            font-size: 0.75rem;
        }

        .right-icons {
            display: flex;
            flex-direction: column;
            align-items: center;
            gap: 12px;
        }

        .icon-with-number {
            display: flex;
            flex-direction: column;
            align-items: center;
            font-size: 0.75rem;
            color: #fff;
        }

        .icon-with-number i {
            font-size: 1.4rem;
            margin-bottom: 2px;
        }

        .side-avatar {
            width: 34px;
            height: 34px;
            border-radius: 50%;
            border: 1.5px solid white;
            object-fit: cover;
        }
    </style>
</head>
<body>

    <div class="phone-frame">
        
        <div class="status-bar">
            <span>11:28</span>
            <div class="icons">
                <i class="fas fa-signal" style="font-size: 12px;"></i>
                <i class="fas fa-wifi" style="font-size: 12px;"></i>
                <i class="fas fa-battery-full" style="font-size: 13px;"></i>
            </div>
        </div>

        <div class="app-screen">
            
            <div class="app-header">
                <div class="back-icon"><i class="fas fa-arrow-left"></i> Back</div>
                <div class="header-title">
                    <div class="server-status-wrap">
                        <span class="server-dot"></span> Server Online
                    </div>
                    HEADLOCK VER2
                    <span class="sub-title">BY NgChiDuc</span>
                </div>
                <div class="menu-icon"><i class="fas fa-bars"></i></div>
            </div>

            <div class="avatar-container">
                <img src="https://images.unsplash.com/photo-1566492031773-4f4e44671857?w=150" alt="Avatar" class="avatar">
                <div class="badge"><i class="fas fa-cog"></i></div>
            </div>

            <div class="controls-panel">
                <div class="control-item">
                    <div class="control-label"><i class="fas fa-crosshairs" style="color: #ff4d4d;"></i> REG LOCK</div>
                    <label class="switch">
                        <input type="checkbox" checked>
                        <span class="slider"></span>
                    </label>
                </div>

                <div class="control-item">
                    <div class="control-label"><i class="fas fa-rocket" style="color: #3b82f6;"></i> OPTIMIZER DEVICE</div>
                    <label class="switch">
                        <input type="checkbox">
                        <span class="slider"></span>
                    </label>
                </div>

                <div class="control-item">
                    <div class="control-label"><i class="fas fa-skull" style="color: #a1a1aa;"></i> HEADLOCK V2</div>
                    <label class="switch">
                        <input type="checkbox" checked>
                        <span class="slider"></span>
                    </label>
                </div>

                <div class="control-item">
                    <div class="control-label"><i class="fas fa-cog" style="color: #e4e4e7;"></i> FIX RUNG</div>
                    <label class="switch">
                        <input type="checkbox" checked>
                        <span class="slider"></span>
                    </label>
                </div>

                <div class="control-item">
                    <div class="control-label"><i class="fas fa-brain" style="color: #ec4899;"></i> EXTRACTLY</div>
                    <label class="switch">
                        <input type="checkbox">
                        <span class="slider"></span>
                    </label>
                </div>

                <div class="control-item">
                    <div class="control-label"><i class="fas fa-fire" style="color: #f97316;"></i> BUFF MÀN</div>
                    <label class="switch">
                        <input type="checkbox">
                        <span class="slider"></span>
                    </label>
                </div>
            </div>

            <div class="import-card">
                <div class="import-title">IMPORT CONFIG</div>
                <button class="import-btn">Chọn File Từ Máy</button>
                <div class="import-sub">Chưa chọn file...</div>
            </div>

        </div>

        <div class="toolbar">
            <div class="comment-box">
                <div class="user-info">hieu <span>· 5-26</span></div>
                APP HEADLOCK VER2 Siêu Bá #xuhuong #headlock
            </div>
            <div class="right-icons">
                <div class="icon-with-number"><i class="far fa-heart" style="color: #ff4d4d;"></i></div>
                <div class="icon-with-number"><i class="far fa-comment"></i> 48</div>
                <div class="icon-with-number"><i class="far fa-bookmark"></i> 9</div>
                <div class="icon-with-number"><i class="fas fa-share"></i> 5</div>
                <img src="https://images.unsplash.com/photo-1535713875002-d1d0cf377fde?w=100" alt="Avatar" class="side-avatar">
            </div>
        </div>

    </div>

</body>
</html>
