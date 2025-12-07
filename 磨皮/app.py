import os
import cv2
import numpy as np
from PIL import Image, ImageEnhance
from flask import Flask, render_template, request, jsonify, send_file
import io
import uuid

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 最大上传16MB
app.config['TEMPLATES_AUTO_RELOAD'] = True  # 模板自动重载

# 创建上传目录
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# 存储处理中的图片信息
image_cache = {}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_image():
    """处理图片上传"""
    if 'file' not in request.files:
        return jsonify({'error': '未选择文件'}), 400
    
    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': '文件名为空'}), 400
    
    if file:
        # 生成唯一ID标识图片
        img_id = str(uuid.uuid4())
        # 读取图片
        img = Image.open(file.stream).convert('RGB')
        # 保存原图到缓存
        image_cache[img_id] = {
            'original': img,
            'processed': img.copy()
        }
        # 生成原图预览
        img_byte_arr = io.BytesIO()
        img.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)
        
        return jsonify({
            'success': True,
            'img_id': img_id,
            'original_url': f'/preview/{img_id}/original'
        })

@app.route('/preview/<img_id>/<img_type>')
def preview_image(img_id, img_type):
    """返回预览图片"""
    if img_id not in image_cache:
        return jsonify({'error': '图片不存在'}), 404
    
    img = image_cache[img_id][img_type]
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG')
    img_byte_arr.seek(0)
    
    return send_file(img_byte_arr, mimetype='image/jpeg')

@app.route('/process', methods=['POST'])
def process_image():
    """处理图片（磨皮+美白+去水印）"""
    data = request.get_json()
    img_id = data.get('img_id')
    smooth_level = int(data.get('smooth', 1))
    bright_level = int(data.get('bright', 1))
    watermark_area = data.get('watermark_area', None)
    
    if img_id not in image_cache:
        return jsonify({'error': '图片不存在'}), 404
    
    # 获取原图
    original_img = image_cache[img_id]['original'].copy()
    img = np.array(original_img)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
    
    # 1. 磨皮处理（根据档位调整模糊程度）
    smooth_strength = smooth_level * 2  # 档位1-10对应强度2-20
    # 双边滤波：保留边缘同时磨皮
    img_smoothed = cv2.bilateralFilter(img, d=9, sigmaColor=smooth_strength, sigmaSpace=smooth_strength)
    
    # 2. 美白处理（调整亮度和对比度）
    bright_strength = bright_level * 0.1  # 档位1-10对应0.1-1.0
    # 转换为PIL处理亮度
    img_pil = Image.fromarray(cv2.cvtColor(img_smoothed, cv2.COLOR_BGR2RGB))
    enhancer = ImageEnhance.Brightness(img_pil)
    img_bright = enhancer.enhance(1 + bright_strength)
    
    # 3. 区域去水印（如果选择了区域）
    if watermark_area and all(key in watermark_area for key in ['x1', 'y1', 'x2', 'y2']):
        x1, y1 = int(watermark_area['x1']), int(watermark_area['y1'])
        x2, y2 = int(watermark_area['x2']), int(watermark_area['y2'])
        # 转换为numpy数组处理
        img_np = np.array(img_bright)
        # 计算区域大小
        h, w = y2 - y1, x2 - x1
        # 使用均值填充去水印区域
        roi = img_np[y1:y2, x1:x2]
        avg_color = np.mean(roi, axis=(0,1)).astype(np.uint8)
        img_np[y1:y2, x1:x2] = avg_color
        # 转换回PIL
        img_processed = Image.fromarray(img_np)
    else:
        img_processed = img_bright
    
    # 更新缓存中的处理后图片
    image_cache[img_id]['processed'] = img_processed
    
    return jsonify({
        'success': True,
        'processed_url': f'/preview/{img_id}/processed'
    })

@app.route('/download/<img_id>')
def download_image(img_id):
    """下载处理后的图片"""
    if img_id not in image_cache:
        return jsonify({'error': '图片不存在'}), 404
    
    img = image_cache[img_id]['processed']
    img_byte_arr = io.BytesIO()
    img.save(img_byte_arr, format='JPEG', quality=95)
    img_byte_arr.seek(0)
    
    return send_file(
        img_byte_arr,
        mimetype='image/jpeg',
        as_attachment=True,
        download_name=f'processed_{img_id[:8]}.jpg'
    )

if __name__ == '__main__':
    # 本地运行，禁用调试模式更安全
    app.run(host='127.0.0.1', port=5000, debug=False)