// 全局变量
let currentImgId = null;
let selectedArea = null;
let isSelectingArea = false;
let startX, startY, endX, endY;

// DOM元素
const fileUpload = document.getElementById('file-upload');
const uploadBtn = document.getElementById('upload-btn');
const uploadStatus = document.getElementById('upload-status');
const controlPanel = document.getElementById('control-panel');
const previewPanel = document.getElementById('preview-panel');
const originalImage = document.getElementById('original-image');
const processedImage = document.getElementById('processed-image');
const smoothSlider = document.getElementById('smooth-slider');
const smoothValue = document.getElementById('smooth-value');
const brightSlider = document.getElementById('bright-slider');
const brightValue = document.getElementById('bright-value');
const selectAreaBtn = document.getElementById('select-area-btn');
const areaStatus = document.getElementById('area-status');
const processBtn = document.getElementById('process-btn');
const downloadBtn = document.getElementById('download-btn');
const areaSelector = document.getElementById('area-selector');
const selectorOverlay = document.getElementById('selector-overlay');
const selectionBox = document.getElementById('selection-box');
const confirmAreaBtn = document.getElementById('confirm-area-btn');
const cancelAreaBtn = document.getElementById('cancel-area-btn');

// 初始化滑块值显示
smoothSlider.addEventListener('input', () => {
    smoothValue.textContent = smoothSlider.value;
});

brightSlider.addEventListener('input', () => {
    brightValue.textContent = brightSlider.value;
});

// 上传图片
uploadBtn.addEventListener('click', async () => {
    const file = fileUpload.files[0];
    if (!file) {
        uploadStatus.textContent = '请先选择图片文件';
        uploadStatus.style.color = 'red';
        return;
    }

    const formData = new FormData();
    formData.append('file', file);

    try {
        const response = await fetch('/upload', {
            method: 'POST',
            body: formData
        });

        const result = await response.json();
        if (result.success) {
            currentImgId = result.img_id;
            originalImage.src = result.original_url + '?t=' + new Date().getTime();
            processedImage.src = '';
            uploadStatus.textContent = '上传成功！';
            uploadStatus.style.color = 'green';
            controlPanel.style.display = 'block';
            previewPanel.style.display = 'block';
            selectedArea = null;
            areaStatus.textContent = '未选择区域';
        } else {
            uploadStatus.textContent = '上传失败：' + result.error;
            uploadStatus.style.color = 'red';
        }
    } catch (error) {
        uploadStatus.textContent = '上传出错：' + error.message;
        uploadStatus.style.color = 'red';
    }
});

// 选择去水印区域
selectAreaBtn.addEventListener('click', () => {
    if (!currentImgId) {
        areaStatus.textContent = '请先上传图片';
        areaStatus.style.color = 'red';
        return;
    }

    areaSelector.style.display = 'flex';
    isSelectingArea = false;
    selectionBox.style.display = 'none';
});

// 区域选择逻辑
selectorOverlay.addEventListener('mousedown', (e) => {
    isSelectingArea = true;
    startX = e.clientX;
    startY = e.clientY;
    selectionBox.style.left = startX + 'px';
    selectionBox.style.top = startY + 'px';
    selectionBox.style.width = '0px';
    selectionBox.style.height = '0px';
    selectionBox.style.display = 'block';
});

selectorOverlay.addEventListener('mousemove', (e) => {
    if (!isSelectingArea) return;
    endX = e.clientX;
    endY = e.clientY;
    
    // 计算选框位置和大小
    const left = Math.min(startX, endX);
    const top = Math.min(startY, endY);
    const width = Math.abs(endX - startX);
    const height = Math.abs(endY - startY);
    
    selectionBox.style.left = left + 'px';
    selectionBox.style.top = top + 'px';
    selectionBox.style.width = width + 'px';
    selectionBox.style.height = height + 'px';
});

selectorOverlay.addEventListener('mouseup', () => {
    isSelectingArea = false;
    if (endX && endY) {
        selectedArea = {
            x1: Math.min(startX, endX),
            y1: Math.min(startY, endY),
            x2: Math.max(startX, endX),
            y2: Math.max(startY, endY)
        };
    }
});

// 确认选择区域
confirmAreaBtn.addEventListener('click', () => {
    areaSelector.style.display = 'none';
    if (selectedArea) {
        areaStatus.textContent = `已选择区域: (${selectedArea.x1},${selectedArea.y1}) - (${selectedArea.x2},${selectedArea.y2})`;
        areaStatus.style.color = 'green';
    } else {
        areaStatus.textContent = '未选择有效区域';
        areaStatus.style.color = 'red';
    }
});

// 取消选择区域
cancelAreaBtn.addEventListener('click', () => {
    areaSelector.style.display = 'none';
    selectedArea = null;
    areaStatus.textContent = '未选择区域';
});

// 处理图片
processBtn.addEventListener('click', async () => {
    if (!currentImgId) {
        alert('请先上传图片');
        return;
    }

    const smoothLevel = smoothSlider.value;
    const brightLevel = brightSlider.value;

    try {
        const response = await fetch('/process', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                img_id: currentImgId,
                smooth: smoothLevel,
                bright: brightLevel,
                watermark_area: selectedArea
            })
        });

        const result = await response.json();
        if (result.success) {
            processedImage.src = result.processed_url + '?t=' + new Date().getTime();
            alert('处理完成！');
        } else {
            alert('处理失败：' + result.error);
        }
    } catch (error) {
        alert('处理出错：' + error.message);
    }
});

// 下载图片
downloadBtn.addEventListener('click', () => {
    if (!currentImgId) {
        alert('请先处理图片');
        return;
    }
    window.open(`/download/${currentImgId}`, '_blank');
});