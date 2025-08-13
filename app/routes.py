import os
import json
import requests
from flask import jsonify, render_template, send_from_directory, Response, abort
from app import app
from config import MODS_FILE, DOWNLOAD_DIR, PROXY_IMAGES, PROXY_VIDEOS

@app.route('/')
def index():
    return render_template('index.html',
                           proxy_images=PROXY_IMAGES,
                           proxy_videos=PROXY_VIDEOS)

@app.route('/api/mods')
def get_mods():
    try:
        with open(MODS_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except FileNotFoundError:
        return jsonify({"error": "Mods data not found. Please wait for the background task to run."}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/download/local/<filename>')
def download_local_mod(filename):
    """从本地服务器下载文件（.py 文件）"""
    try:
        return send_from_directory(
            os.path.abspath(DOWNLOAD_DIR), 
            filename, 
            as_attachment=True
        )
    except FileNotFoundError:
        return "File not found.", 404
    except Exception as e:
        return f"Error downloading file: {e}", 500

@app.route('/download/proxy/<file_id>/<filename>')
def download_proxy_mod(file_id, filename):
    """反向代理下载文件（图片、视频等）"""
    is_image = any(filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif'])
    is_video = any(filename.lower().endswith(ext) for ext in ['.mp4', '.webm', '.mov'])

    if (is_image and not PROXY_IMAGES) or (is_video and not PROXY_VIDEOS):
        abort(403, description="Proxy for this file type is disabled.")

    try:
        download_url = f"https://mods.ballistica.workers.dev/getFile?fileId={file_id}"
        req = requests.get(download_url, stream=True)
        req.raise_for_status()
        
        response_headers = {
            "Content-Disposition": f"attachment; filename={filename}",
            "Cross-Origin-Resource-Policy": "cross-origin"
        }
        return Response(req.iter_content(chunk_size=8192),
                        content_type=req.headers['Content-Type'],
                        headers=response_headers)
    except requests.exceptions.RequestException as e:
        return f"Error downloading file: {e}", 500