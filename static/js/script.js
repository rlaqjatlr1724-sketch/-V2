// ============================================================================
// State Management
// ============================================================================
const state = {
    files: [],
    stores: [],
    selectedStoreId: null,
    currentTab: 'upload',
    conversationHistory: [],
    currentLanguage: 'ko'
};

// ============================================================================
// Translations
// ============================================================================
const translations = {
    ko: {
        // Navigation
        'nav_chat_search': '올공이 챗봇',
        'nav_map_category': '올공이 지도',
        'nav_map_guide': '올림픽공원 약도',
        'nav_nearest_facility': '가까운 시설물',

        // Section Headers
        'company_name': '한국체육산업개발(주)',
        'wayfinding_header': '올림픽공원 길찾기',
        'wayfinding_subtitle': '지도를 클릭하여 출발지와 도착지를 선택하세요 (파란색: 출발, 초록색: 도착)',
        'facility_header': '가장 가까운 시설물 찾기',
        'facility_subtitle': '지도에서 현재 위치를 클릭하면 가장 가까운 시설물로 안내합니다',

        // Mascot Greeting
        'mascot_greeting': '안녕하세요! 올림픽 공원 AI 챗봇 올공이 입니다!',
        'mascot_warning': 'AI assistant는 잘못된 답변을 제공할 수 있습니다. 자세한 문의는 고객센터를 이용하여 주세요.',
        'mascot_contact': '종합안내 : 02-410-1114',

        // Buttons
        'btn_select_all': 'Select All',
        'btn_clear_chat': 'Clear Chat',
        'btn_send': 'Send',
        'btn_reset': '초기화',
        'btn_close': '닫기',

        // Search Panel
        'select_filestore': 'Select FileStore to Search',
        'conversation': 'Conversation',
        'no_conversation': 'No conversation yet. Start by asking a question!',
        'ask_question': 'Ask a question about your documents...',
        'searching': 'Searching...',

        // Map Guide
        'map_title': '올림픽공원 지도',
        'first_click': '첫 번째 클릭: 출발지',
        'second_click': '두 번째 클릭: 도착지',
        'click_start': '지도를 클릭하여 출발지를 선택하세요',
        'click_destination': '지도를 클릭하여 도착지를 선택하세요',
        'calculating': '경로를 계산하는 중...',
        'path_found': '경로를 찾았습니다! 초기화하여 다시 시작할 수 있습니다.',
        'path_result': '경로 결과',
        'departure': '출발:',
        'arrival': '도착:',
        'distance': '거리:',

        // Facility Search
        'facility_type': '시설물 종류',
        'toilet': '화장실',
        'store': '매점(편의점)',
        'water': '음수대',
        'parking': '주차 사전무인정산기',
        'click_location': '지도를 클릭하여 현재 위치를 선택하세요',
        'finding_facility': '가장 가까운 시설물을 찾는 중...',
        'facility_found': '가장 가까운 시설물로의 경로를 찾았습니다!',

        // Empty States
        'no_filestores': 'No FileStores available'
    },
    en: {
        // Navigation
        'nav_chat_search': 'Olgongi Chatbot',
        'nav_map_category': 'Olgongi Map',
        'nav_map_guide': 'Olympic Park Map',
        'nav_nearest_facility': 'Nearest Facility',

        // Section Headers
        'company_name': 'Korea Sports Industry Development Co., Ltd.',
        'wayfinding_header': 'Olympic Park Wayfinding',
        'wayfinding_subtitle': 'Click on the map to select start and destination (Blue: Start, Green: Destination)',
        'facility_header': 'Find Nearest Facility',
        'facility_subtitle': 'Click your current location on the map to find the nearest facility',

        // Mascot Greeting
        'mascot_greeting': 'Hello! I am Olgongi, the Olympic Park AI Chatbot!',
        'mascot_warning': 'AI assistant may provide incorrect answers. Please contact customer service for detailed inquiries.',
        'mascot_contact': 'General Information: 02-410-1114',

        // Buttons
        'btn_select_all': 'Select All',
        'btn_clear_chat': 'Clear Chat',
        'btn_send': 'Send',
        'btn_reset': 'Reset',
        'btn_close': 'Close',

        // Search Panel
        'select_filestore': 'Select FileStore to Search',
        'conversation': 'Conversation',
        'no_conversation': 'No conversation yet. Start by asking a question!',
        'ask_question': 'Ask a question about your documents...',
        'searching': 'Searching...',

        // Map Guide
        'map_title': 'Olympic Park Map',
        'first_click': 'First Click: Start',
        'second_click': 'Second Click: Destination',
        'click_start': 'Click on the map to select start location',
        'click_destination': 'Click on the map to select destination',
        'calculating': 'Calculating route...',
        'path_found': 'Route found! Reset to start over.',
        'path_result': 'Route Result',
        'departure': 'Start:',
        'arrival': 'Destination:',
        'distance': 'Distance:',

        // Facility Search
        'facility_type': 'Facility Type',
        'toilet': 'Restroom',
        'store': 'Store (Convenience)',
        'water': 'Water Fountain',
        'parking': 'Parking Pre-Payment Kiosk',
        'click_location': 'Click on the map to select your location',
        'finding_facility': 'Finding nearest facility...',
        'facility_found': 'Found route to nearest facility!',

        // Empty States
        'no_filestores': 'No FileStores available'
    },
    zh: {
        // Navigation
        'nav_chat_search': '奥公聊天机器人',
        'nav_map_category': '奥公地图',
        'nav_map_guide': '奥林匹克公园地图',
        'nav_nearest_facility': '最近设施',

        // Section Headers
        'company_name': '韩国体育产业开发株式会社',
        'wayfinding_header': '奥林匹克公园路线导航',
        'wayfinding_subtitle': '点击地图选择起点和终点（蓝色：起点，绿色：终点）',
        'facility_header': '查找最近设施',
        'facility_subtitle': '在地图上点击您的当前位置以查找最近的设施',

        // Mascot Greeting
        'mascot_greeting': '您好！我是奥林匹克公园AI聊天机器人奥公！',
        'mascot_warning': 'AI助手可能提供不正确的答案。详细咨询请联系客服中心。',
        'mascot_contact': '综合咨询：02-410-1114',

        // Buttons
        'btn_select_all': 'Select All',
        'btn_clear_chat': 'Clear Chat',
        'btn_send': 'Send',
        'btn_reset': '重置',
        'btn_close': '关闭',

        // Search Panel
        'select_filestore': 'Select FileStore to Search',
        'conversation': 'Conversation',
        'no_conversation': 'No conversation yet. Start by asking a question!',
        'ask_question': 'Ask a question about your documents...',
        'searching': 'Searching...',

        // Map Guide
        'map_title': '奥林匹克公园地图',
        'first_click': '第一次点击：起点',
        'second_click': '第二次点击：终点',
        'click_start': '点击地图选择起点',
        'click_destination': '点击地图选择终点',
        'calculating': '正在计算路线...',
        'path_found': '找到路线！重置以重新开始。',
        'path_result': '路线结果',
        'departure': '起点：',
        'arrival': '终点：',
        'distance': '距离：',

        // Facility Search
        'facility_type': '设施类型',
        'toilet': '洗手间',
        'store': '商店（便利店）',
        'water': '饮水机',
        'parking': '停车预付费机',
        'click_location': '点击地图选择您的位置',
        'finding_facility': '正在查找最近的设施...',
        'facility_found': '找到前往最近设施的路线！',

        // Empty States
        'no_filestores': 'No FileStores available'
    },
    ja: {
        // Navigation
        'nav_chat_search': 'オルゴンイチャットボット',
        'nav_map_category': 'オルゴンイマップ',
        'nav_map_guide': 'オリンピック公園地図',
        'nav_nearest_facility': '最寄りの施設',

        // Section Headers
        'company_name': '韓国体育産業開発株式会社',
        'wayfinding_header': 'オリンピック公園道案内',
        'wayfinding_subtitle': '地図をクリックして出発地と目的地を選択してください（青：出発、緑：目的地）',
        'facility_header': '最寄りの施設を検索',
        'facility_subtitle': '地図上で現在地をクリックして最寄りの施設をご案内します',

        // Mascot Greeting
        'mascot_greeting': 'こんにちは！オリンピック公園AIチャットボットのオルゴンイです！',
        'mascot_warning': 'AIアシスタントは誤った回答を提供する可能性があります。詳細なお問い合わせはカスタマーサービスをご利用ください。',
        'mascot_contact': '総合案内：02-410-1114',

        // Buttons
        'btn_select_all': 'Select All',
        'btn_clear_chat': 'Clear Chat',
        'btn_send': 'Send',
        'btn_reset': 'リセット',
        'btn_close': '閉じる',

        // Search Panel
        'select_filestore': 'Select FileStore to Search',
        'conversation': 'Conversation',
        'no_conversation': 'No conversation yet. Start by asking a question!',
        'ask_question': 'Ask a question about your documents...',
        'searching': 'Searching...',

        // Map Guide
        'map_title': 'オリンピック公園地図',
        'first_click': '最初のクリック：出発地',
        'second_click': '2回目のクリック：目的地',
        'click_start': '地図をクリックして出発地を選択',
        'click_destination': '地図をクリックして目的地を選択',
        'calculating': 'ルートを計算中...',
        'path_found': 'ルートが見つかりました！リセットして再開できます。',
        'path_result': 'ルート結果',
        'departure': '出発：',
        'arrival': '目的地：',
        'distance': '距離：',

        // Facility Search
        'facility_type': '施設タイプ',
        'toilet': 'トイレ',
        'store': '売店（コンビニ）',
        'water': '飲水台',
        'parking': '駐車場事前精算機',
        'click_location': '地図をクリックして現在地を選択',
        'finding_facility': '最寄りの施設を検索中...',
        'facility_found': '最寄りの施設へのルートを見つけました！',

        // Empty States
        'no_filestores': 'No FileStores available'
    },
    vi: {
        // Navigation
        'nav_chat_search': 'Chatbot Olgongi',
        'nav_map_category': 'Bản đồ Olgongi',
        'nav_map_guide': 'Bản đồ Công viên Olympic',
        'nav_nearest_facility': 'Cơ sở Gần nhất',

        // Section Headers
        'company_name': 'Công ty Phát triển Công nghiệp Thể thao Hàn Quốc',
        'wayfinding_header': 'Chỉ đường Công viên Olympic',
        'wayfinding_subtitle': 'Nhấp vào bản đồ để chọn điểm bắt đầu và đích (Xanh dương: Bắt đầu, Xanh lá: Đích)',
        'facility_header': 'Tìm Cơ sở Gần nhất',
        'facility_subtitle': 'Nhấp vào vị trí hiện tại của bạn trên bản đồ để tìm cơ sở gần nhất',

        // Mascot Greeting
        'mascot_greeting': 'Xin chào! Tôi là Olgongi, Chatbot AI Công viên Olympic!',
        'mascot_warning': 'Trợ lý AI có thể cung cấp câu trả lời không chính xác. Vui lòng liên hệ dịch vụ khách hàng để biết thêm chi tiết.',
        'mascot_contact': 'Thông tin chung: 02-410-1114',

        // Buttons
        'btn_select_all': 'Select All',
        'btn_clear_chat': 'Clear Chat',
        'btn_send': 'Send',
        'btn_reset': 'Đặt lại',
        'btn_close': 'Đóng',

        // Search Panel
        'select_filestore': 'Select FileStore to Search',
        'conversation': 'Conversation',
        'no_conversation': 'No conversation yet. Start by asking a question!',
        'ask_question': 'Ask a question about your documents...',
        'searching': 'Searching...',

        // Map Guide
        'map_title': 'Bản đồ Công viên Olympic',
        'first_click': 'Nhấp đầu tiên: Bắt đầu',
        'second_click': 'Nhấp thứ hai: Đích',
        'click_start': 'Nhấp vào bản đồ để chọn vị trí bắt đầu',
        'click_destination': 'Nhấp vào bản đồ để chọn đích',
        'calculating': 'Đang tính toán tuyến đường...',
        'path_found': 'Đã tìm thấy tuyến đường! Đặt lại để bắt đầu lại.',
        'path_result': 'Kết quả Tuyến đường',
        'departure': 'Bắt đầu:',
        'arrival': 'Đích:',
        'distance': 'Khoảng cách:',

        // Facility Search
        'facility_type': 'Loại Cơ sở',
        'toilet': 'Nhà vệ sinh',
        'store': 'Cửa hàng (Tiện lợi)',
        'water': 'Vòi nước uống',
        'parking': 'Máy Thanh toán Trước Bãi đỗ xe',
        'click_location': 'Nhấp vào bản đồ để chọn vị trí của bạn',
        'finding_facility': 'Đang tìm cơ sở gần nhất...',
        'facility_found': 'Đã tìm thấy tuyến đường đến cơ sở gần nhất!',

        // Empty States
        'no_filestores': 'No FileStores available'
    }
};

// ============================================================================
// DOM Elements
// ============================================================================
const uploadArea = document.getElementById('uploadArea');
const fileInput = document.getElementById('fileInput');
const uploadProgress = document.getElementById('uploadProgress');
const uploadStatus = document.getElementById('uploadStatus');
const filesList = document.getElementById('filesList');
const fileCheckboxList = document.getElementById('fileCheckboxList');
const searchQuery = document.getElementById('searchQuery');
const searchBtn = document.getElementById('searchBtn');
const searchLoading = document.getElementById('searchLoading');
const toast = document.getElementById('toast');
const refreshFilesBtn = document.getElementById('refreshFilesBtn');
const selectAllBtn = document.getElementById('selectAllBtn');
const chatHistory = document.getElementById('chatHistory');
const clearChatBtn = document.getElementById('clearChatBtn');

// ============================================================================
// Initialization
// ============================================================================
document.addEventListener('DOMContentLoaded', () => {
    setupEventListeners();

    // Only load files if the filesList element exists
    if (filesList) {
        loadFiles();
    }

    loadStores();
});

// ============================================================================
// Event Listeners Setup
// ============================================================================
function setupEventListeners() {
    // Tab navigation
    document.querySelectorAll('.nav-item[data-tab]').forEach(item => {
        item.addEventListener('click', handleTabChange);
    });

    // Navigation group toggle
    const mapGroupHeader = document.getElementById('mapGroupHeader');
    const mapGroupContent = document.getElementById('mapGroupContent');

    if (mapGroupHeader && mapGroupContent) {
        mapGroupHeader.addEventListener('click', () => {
            mapGroupHeader.classList.toggle('expanded');
            mapGroupContent.classList.toggle('expanded');
        });

        // 기본적으로 확장된 상태로 시작
        mapGroupHeader.classList.add('expanded');
        mapGroupContent.classList.add('expanded');
    }

    // File upload (only if elements exist)
    if (uploadArea && fileInput) {
        uploadArea.addEventListener('click', () => fileInput.click());
        uploadArea.addEventListener('dragover', handleDragOver);
        uploadArea.addEventListener('dragleave', handleDragLeave);
        uploadArea.addEventListener('drop', handleDrop);
        fileInput.addEventListener('change', handleFileSelect);
    }

    // File list
    if (refreshFilesBtn) {
        refreshFilesBtn.addEventListener('click', loadFiles);
    }

    // Search
    if (searchBtn) {
        searchBtn.addEventListener('click', performSearch);
    }
    if (selectAllBtn) {
        selectAllBtn.addEventListener('click', toggleSelectAll);
    }
    if (clearChatBtn) {
        clearChatBtn.addEventListener('click', clearConversation);
    }

    // Search with Enter (without Ctrl for better UX)
    if (searchQuery) {
        searchQuery.addEventListener('keydown', (e) => {
            // Shift+Enter for new line, Enter alone to send
            if (e.key === 'Enter' && !e.shiftKey) {
                e.preventDefault();
                performSearch();
            }
        });
    }

    // Import panel buttons
    const confirmImportBtn = document.getElementById('confirmImportBtn');
    const cancelImportBtn = document.getElementById('cancelImportBtn');

    if (confirmImportBtn) {
        confirmImportBtn.addEventListener('click', confirmImportFile);
    }
    if (cancelImportBtn) {
        cancelImportBtn.addEventListener('click', cancelImportPanel);
    }

    // FileStore selection update
    const storeSelectForUpload = document.getElementById('storeSelectForUpload');
    if (storeSelectForUpload) {
        storeSelectForUpload.addEventListener('change', () => {
            // Simple handler for store selection
        });
    }
}

// ============================================================================
// Tab Management
// ============================================================================
function handleTabChange(e) {
    const tabName = e.currentTarget.getAttribute('data-tab');

    // Update navigation
    document.querySelectorAll('.nav-item').forEach(item => {
        item.classList.remove('active');
    });
    e.currentTarget.classList.add('active');

    // Update tab content
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    document.getElementById(tabName).classList.add('active');

    state.currentTab = tabName;

    // Tab-specific initialization
    if (tabName === 'files') {
        loadFiles();
    } else if (tabName === 'stores') {
        loadStores();
    } else if (tabName === 'search') {
        loadStores();
    }
}

// ============================================================================
// File Upload (Drag and Drop)
// ============================================================================
function handleDragOver(e) {
    e.preventDefault();
    uploadArea.classList.add('drag-over');
}

function handleDragLeave(e) {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
}

function handleDrop(e) {
    e.preventDefault();
    uploadArea.classList.remove('drag-over');
    const files = e.dataTransfer.files;
    handleFiles(files);
}

function handleFileSelect(e) {
    const files = e.target.files;
    handleFiles(files);
}

function handleFiles(files) {
    const fileArray = Array.from(files);
    uploadProgress.style.display = 'block';
    uploadStatus.innerHTML = '';

    fileArray.forEach((file, index) => {
        uploadFile(file, index, fileArray.length);
    });
}

// ============================================================================
// File Upload to Files API (My Files)
// ============================================================================
async function uploadFile(file, index, total) {
    const formData = new FormData();
    formData.append('file', file);

    const fileName = file.name;
    const statusItem = document.createElement('div');
    statusItem.className = 'status-item';
    statusItem.id = `status-${index}`;
    statusItem.innerHTML = `
        <div class="status-icon">⏳</div>
        <div class="status-content">
            <div class="status-title">${fileName}</div>
            <div class="status-message">Uploading...</div>
        </div>
    `;
    uploadStatus.appendChild(statusItem);

    try {
        const uploadResponse = await fetch('/api/files/upload', {
            method: 'POST',
            body: formData
        });

        const uploadData = await uploadResponse.json();

        if (!uploadData.success) {
            throw new Error(uploadData.error || 'Upload failed');
        }

        // Show upload success
        statusItem.classList.add('success');
        statusItem.innerHTML = `
            <div class="status-icon">✓</div>
            <div class="status-content">
                <div class="status-title">${fileName}</div>
                <div class="status-message">Upload completed to My Files</div>
            </div>
        `;
        showToast(`${fileName} uploaded successfully to My Files`, 'success');

        // Refresh file list when all uploads complete
        if (document.querySelectorAll('.status-item.success').length === total) {
            setTimeout(() => {
                loadFiles();
                loadStores();
                uploadProgress.style.display = 'none';
            }, 1000);
        }
    } catch (error) {
        statusItem.classList.add('error');
        statusItem.innerHTML = `
            <div class="status-icon">✗</div>
            <div class="status-content">
                <div class="status-title">${fileName}</div>
                <div class="status-message">${error.message}</div>
            </div>
        `;
        showToast(`${fileName} upload failed: ${error.message}`, 'error');
    }
}

// ============================================================================
// File Management
// ============================================================================
async function loadFiles() {
    if (!filesList) return; // Exit if element doesn't exist

    try {
        const response = await fetch('/api/files');
        const data = await response.json();

        if (data.success) {
            state.files = data.files;
            renderFiles();
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        console.error('Error loading files:', error);
        if (filesList) {
            filesList.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">❌</div>
                    <p>Failed to load files: ${error.message}</p>
                </div>
            `;
        }
    }
}

function renderFiles() {
    if (!filesList) return; // Exit if element doesn't exist

    if (state.files.length === 0) {
        filesList.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">📭</div>
                <p>No uploaded files yet</p>
            </div>
        `;
        return;
    }

    filesList.innerHTML = state.files.map(file => {
        const sizeInMB = (file.size_bytes / (1024 * 1024)).toFixed(2);
        const fileName = file.display_name;
        const date = new Date(file.create_time).toLocaleDateString('en-US');
        const fileId = file.file_id;

        return `
            <div class="file-card">
                <div class="file-card-header">
                    <div class="file-icon">${getFileIcon(fileName)}</div>
                    <div class="file-card-actions">
                        <button title="Move to FileStore" onclick="showImportPanel('${fileId}', '${fileName}')">📤</button>
                        <button title="Delete" onclick="deleteFile('${fileId}', '${fileName}')">🗑️</button>
                    </div>
                </div>
                <div class="file-name" title="${fileName}">${fileName}</div>
                <div class="file-info">
                    <span>${sizeInMB} MB</span>
                    <span class="file-date">${date}</span>
                </div>
            </div>
        `;
    }).join('');
}

function getFileIcon(fileName) {
    const ext = fileName.split('.').pop().toLowerCase();
    const iconMap = {
        'pdf': '📄',
        'txt': '📝',
        'doc': '📘',
        'docx': '📘',
        'xls': '📊',
        'xlsx': '📊',
        'ppt': '🎨',
        'pptx': '🎨',
        'csv': '📋',
        'json': '{}',
        'xml': '<>',
        'html': '🌐'
    };
    return iconMap[ext] || '📎';
}

async function deleteFile(fileId, fileName) {
    if (!confirm(`Delete "${fileName}"?`)) {
        return;
    }

    try {
        const response = await fetch(`/api/files/${fileId}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (data.success) {
            showToast(`${fileName} deleted successfully`, 'success');
            loadFiles();
            loadStores();
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        showToast(`Delete failed: ${error.message}`, 'error');
    }
}

// File preview
async function previewFile(fileId, fileName) {
    try {
        const cleanFileId = fileId.replace(/^files\//, '');
        const response = await fetch(`/api/files/${cleanFileId}/preview`);
        const data = await response.json();

        if (!data.success) {
            showToast(`Preview unavailable: ${data.error}`, 'error');
            return;
        }

        // Files API files cannot be accessed directly in browser
        // Show file information instead
        const sizeInMB = (data.size_bytes / 1024 / 1024).toFixed(2);
        const createTime = data.create_time ? new Date(data.create_time).toLocaleString('ko-KR') : 'Unknown';

        alert(
            `File Information:\n\n` +
            `Name: ${fileName}\n` +
            `Type: ${data.mime_type || 'Unknown'}\n` +
            `Size: ${sizeInMB} MB\n` +
            `Created: ${createTime}\n\n` +
            `Note: Files in "My Files" cannot be previewed directly.\n` +
            `Please import to FileStore to use in search.`
        );

        showToast(`Showing ${fileName} information`, 'info');
    } catch (error) {
        showToast(`Preview error: ${error.message}`, 'error');
    }
}

// ============================================================================
// FileSearchStore Management
// ============================================================================
async function loadStores() {
    try {
        const response = await fetch('/api/stores');
        const data = await response.json();

        if (data.success) {
            state.stores = data.stores;
            renderStores();
            renderStoresForSearch();
            updateStoreSelects();
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        console.error('Error loading stores:', error);
        const storesContainer = document.getElementById('storesList');
        if (storesContainer) {
            storesContainer.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">❌</div>
                    <p>Failed to load stores: ${error.message}</p>
                </div>
            `;
        }
    }
}

function updateStoreSelects() {
    // Update main upload storeSelect
    const storeSelect = document.getElementById('storeSelect');
    if (storeSelect) {
        const selectedValue = storeSelect.value;
        storeSelect.innerHTML = '<option value="">Select FileStore...</option>';

        state.stores.forEach(store => {
            const option = document.createElement('option');
            option.value = store.store_name;
            option.textContent = store.display_name;
            storeSelect.appendChild(option);
        });

        if (selectedValue) {
            storeSelect.value = selectedValue;
        }
    }

    // Update FileStore tab storeSelectForUpload
    const storeSelectForUpload = document.getElementById('storeSelectForUpload');
    if (storeSelectForUpload) {
        const selectedValue = storeSelectForUpload.value;
        storeSelectForUpload.innerHTML = '<option value="">Select FileStore...</option>';

        state.stores.forEach(store => {
            const option = document.createElement('option');
            option.value = store.store_name;
            option.textContent = store.display_name;
            storeSelectForUpload.appendChild(option);
        });

        if (selectedValue) {
            storeSelectForUpload.value = selectedValue;
        }
    }
}

function renderStores() {
    const storesContainer = document.getElementById('storesList');
    if (!storesContainer) return;

    if (state.stores.length === 0) {
        storesContainer.innerHTML = `
            <div class="create-store-form">
                <h3>Create New FileSearchStore</h3>
                <input type="text" id="newStoreName" placeholder="Store name (e.g., Document Store)" class="input-field">
                <button class="btn btn-primary" onclick="createStore()">Create</button>
            </div>
            <div class="empty-state">
                <div class="empty-icon">💾</div>
                <p>No FileSearchStores created yet</p>
            </div>
        `;
        return;
    }

    const storeCards = state.stores.map(store => {
        const activeCount = store.active_documents_count || 0;
        const pendingCount = store.pending_documents_count || 0;
        const failedCount = store.failed_documents_count || 0;
        const totalSize = store.size_bytes || 0;
        const sizeInMB = (totalSize / (1024 * 1024)).toFixed(2);
        const createdDate = new Date(store.create_time).toLocaleDateString('en-US');

        return `
            <div class="store-card" onclick="showStoreDocuments('${store.store_name}', '${store.display_name}')">
                <div class="store-header">
                    <h3>${store.display_name}</h3>
                    <button class="btn btn-danger btn-sm" onclick="event.stopPropagation(); deleteStore('${store.store_name}', '${store.display_name}')">Delete</button>
                </div>
                <div class="store-info">
                    <div class="store-stat">
                        <span class="store-label">Active Documents:</span>
                        <span class="store-value file-count-${store.store_name.replace(/\//g, '-')}">${activeCount}</span>
                    </div>
                    <div class="store-stat">
                        <span class="store-label">Processing:</span>
                        <span class="store-value">${pendingCount}</span>
                    </div>
                    ${failedCount > 0 ? `
                    <div class="store-stat">
                        <span class="store-label">Failed:</span>
                        <span class="store-value error">${failedCount}</span>
                    </div>
                    ` : ''}
                    <div class="store-stat">
                        <span class="store-label">Storage:</span>
                        <span class="store-value">${sizeInMB} MB</span>
                    </div>
                    <div class="store-stat">
                        <span class="store-label">Created:</span>
                        <span class="store-value">${createdDate}</span>
                    </div>
                    <div class="store-stat">
                        <span class="store-label">Store ID:</span>
                        <span class="store-value store-id" style="font-size: 12px;">${store.store_name}</span>
                    </div>
                </div>
            </div>
        `;
    }).join('');

    storesContainer.innerHTML = `
        <div class="create-store-form">
            <h3>Create New FileSearchStore</h3>
            <input type="text" id="newStoreName" placeholder="Store name (e.g., Document Store)" class="input-field">
            <button class="btn btn-primary" onclick="createStore()">Create</button>
        </div>
        <div class="stores-grid">
            ${storeCards}
        </div>
    `;

    updateStats();
}

function updateStats() {
    const totalFilesElem = document.getElementById('totalFiles');
    const totalSizeElem = document.getElementById('totalSize');

    // Only update if elements exist
    if (!totalFilesElem || !totalSizeElem) return;

    const totalActiveDocuments = state.stores.reduce((sum, s) => sum + (s.active_documents_count || 0), 0);
    totalFilesElem.textContent = totalActiveDocuments;

    const totalBytes = state.stores.reduce((sum, s) => sum + (s.size_bytes || 0), 0);
    const totalSize = (totalBytes / (1024 * 1024)).toFixed(2);
    totalSizeElem.textContent = totalSize + ' MB';
}

async function createStore() {
    const nameInput = document.getElementById('newStoreName');
    const name = nameInput.value.trim();

    if (!name) {
        showToast('Please enter a store name', 'warning');
        return;
    }

    try {
        const response = await fetch('/api/stores/create', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ name })
        });

        const data = await response.json();

        if (data.success) {
            showToast(`FileStore "${name}" created successfully`, 'success');
            nameInput.value = '';
            loadStores();
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        showToast(`Failed to create store: ${error.message}`, 'error');
    }
}

async function deleteStore(storeId, storeName) {
    if (!confirm(`Delete FileStore "${storeName}"?\nFiles will be preserved.`)) {
        return;
    }

    try {
        const response = await fetch(`/api/stores/${storeId}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (data.success) {
            showToast(`FileStore "${storeName}" deleted successfully`, 'success');
            loadStores();
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        showToast(`Failed to delete store: ${error.message}`, 'error');
    }
}

// ============================================================================
// Search Functionality
// ============================================================================
function renderStoresForSearch() {
    const container = fileCheckboxList;
    if (!container) return;

    if (state.stores.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <p>No FileSearchStores available</p>
                <small>Create a store in the FileStore tab</small>
            </div>
        `;
        return;
    }

    const storeRadios = state.stores.map((store, index) => {
        const fileCount = store.active_documents_count || 0;
        const checked = index === 0 ? 'checked' : '';

        return `
            <label class="checkbox-item">
                <input type="radio" name="store" value="${store.store_name}" class="store-radio" ${checked}>
                <span class="checkbox-label">${store.display_name}</span>
                <span class="checkbox-size">${fileCount} documents</span>
            </label>
        `;
    }).join('');

    container.innerHTML = storeRadios;

    if (state.stores.length > 0) {
        state.selectedStoreId = state.stores[0].store_name;
    }

    document.querySelectorAll('.store-radio').forEach(radio => {
        radio.addEventListener('change', (e) => {
            state.selectedStoreId = e.target.value;
        });
    });
}

function toggleSelectAll() {
    showToast('Only one store can be selected', 'info');
}

async function performSearch() {
    // Check if required elements exist
    if (!searchQuery || !searchLoading || !chatHistory) {
        console.error('Required search elements not found');
        return;
    }

    const selectedRadio = document.querySelector('.store-radio:checked');

    if (!selectedRadio) {
        showToast('Please select a FileStore to search', 'warning');
        return;
    }

    const query = searchQuery.value.trim();
    if (!query) {
        showToast('Please enter a search question', 'warning');
        return;
    }

    const storeId = selectedRadio.value;

    // Add user message to UI immediately
    addMessageToChat('user', query);
    searchQuery.value = '';
    searchLoading.style.display = 'flex';

    try {
        const requestData = {
            query: query,
            store_ids: [storeId],
            metadata_filter: null,
            history: state.conversationHistory
        };

        console.log('Sending request:', requestData);

        const response = await fetch('/api/search', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(requestData)
        });

        const data = await response.json();

        console.log('Response:', data);

        if (data.success) {
            // Add AI response to conversation history and UI
            addMessageToChat('model', data.result);

            // Update conversation history for Gemini API
            state.conversationHistory.push({
                role: 'user',
                parts: [query]
            });
            state.conversationHistory.push({
                role: 'model',
                parts: [data.result]
            });

            console.log('Conversation history updated:', state.conversationHistory);

            showToast('Search completed', 'success');
        } else {
            console.error('Search failed:', data.error);
            throw new Error(data.error);
        }
    } catch (error) {
        console.error('Search error:', error);
        showToast(`Search failed: ${error.message}`, 'error');
        // Remove the user message on error
        const messages = chatHistory.querySelectorAll('.chat-message');
        if (messages.length > 0) {
            messages[messages.length - 1].remove();
        }
    } finally {
        searchLoading.style.display = 'none';
    }
}

function addMessageToChat(role, text) {
    if (!chatHistory) return;

    // Remove empty state if present
    const emptyState = chatHistory.querySelector('.empty-chat');
    if (emptyState) {
        emptyState.remove();
    }

    const messageDiv = document.createElement('div');
    messageDiv.className = `chat-message ${role}-message`;

    const avatarDiv = document.createElement('div');
    avatarDiv.className = 'message-avatar';

    // 사용자는 랜덤 이모지, 모델은 마스코트 프로필 이미지 사용
    if (role === 'user') {
        // 올림픽공원 관련 랜덤 이모지
        const userEmojis = ['🏊', '📖', '🌹', '🎾', '⚽', '🏅'];
        const randomEmoji = userEmojis[Math.floor(Math.random() * userEmojis.length)];
        avatarDiv.textContent = randomEmoji;
    } else {
        const avatarImg = document.createElement('img');
        avatarImg.src = '/static/images/mascot_profile.png';
        avatarImg.alt = '백호돌이';
        avatarImg.className = 'avatar-image';
        avatarDiv.appendChild(avatarImg);
    }

    const contentDiv = document.createElement('div');
    contentDiv.className = 'message-content';

    const textDiv = document.createElement('div');
    textDiv.className = 'message-text';
    textDiv.textContent = text;

    const timeDiv = document.createElement('div');
    timeDiv.className = 'message-time';
    timeDiv.textContent = new Date().toLocaleTimeString('ko-KR', {
        hour: '2-digit',
        minute: '2-digit'
    });

    contentDiv.appendChild(textDiv);
    contentDiv.appendChild(timeDiv);
    messageDiv.appendChild(avatarDiv);
    messageDiv.appendChild(contentDiv);

    chatHistory.appendChild(messageDiv);

    // Scroll to bottom
    chatHistory.scrollTop = chatHistory.scrollHeight;
}

function clearConversation() {
    if (!confirm('Clear all conversation history?')) {
        return;
    }

    state.conversationHistory = [];

    if (chatHistory) {
        chatHistory.innerHTML = `
            <div class="empty-chat">
                <p>No conversation yet. Start by asking a question!</p>
            </div>
        `;
    }

    showToast('Conversation cleared', 'success');
}

// ============================================================================
// Direct FileStore Upload
// ============================================================================
document.addEventListener('DOMContentLoaded', () => {
    const uploadToStoreArea = document.getElementById('uploadToStoreArea');
    const fileInputForStore = document.getElementById('fileInputForStore');

    if (uploadToStoreArea && fileInputForStore) {
        uploadToStoreArea.addEventListener('click', () => fileInputForStore.click());
        uploadToStoreArea.addEventListener('dragover', handleDragOver);
        uploadToStoreArea.addEventListener('dragleave', handleDragLeave);
        uploadToStoreArea.addEventListener('drop', (e) => handleDropForStore(e));
        fileInputForStore.addEventListener('change', handleFileSelectForStore);
    }
});

function handleDropForStore(e) {
    handleDragLeave(e);
    const files = e.dataTransfer.files;

    if (files.length > 0) {
        const store = document.getElementById('storeSelectForUpload').value;
        if (!store) {
            showToast('Please select a FileStore first', 'error');
            return;
        }

        Array.from(files).forEach(file => {
            uploadToFileSearchStore(file, store);
        });
    }
}

function handleFileSelectForStore(e) {
    const store = document.getElementById('storeSelectForUpload').value;
    if (!store) {
        showToast('Please select a FileStore first', 'error');
        return;
    }

    Array.from(e.target.files).forEach(file => {
        uploadToFileSearchStore(file, store);
    });
}

async function uploadToFileSearchStore(file, storeName) {
    const validExtensions = ['pdf', 'txt', 'doc', 'docx', 'xlsx', 'xls', 'ppt', 'pptx', 'csv', 'json', 'xml', 'html'];
    const ext = file.name.split('.').pop().toLowerCase();

    if (!validExtensions.includes(ext)) {
        showToast(`Unsupported file format: ${file.name}`, 'error');
        return;
    }

    const uploadProgress = document.getElementById('uploadToStoreProgress');
    const uploadStatus = document.getElementById('uploadToStoreStatus');
    const progressFill = document.getElementById('progressFillStore');
    const uploadFileName = document.getElementById('uploadToStoreFileName');

    uploadFileName.textContent = `Uploading ${file.name}...`;
    uploadProgress.style.display = 'block';
    uploadStatus.innerHTML = '';

    try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('store_name', storeName);

        const xhr = new XMLHttpRequest();

        xhr.upload.addEventListener('progress', (e) => {
            if (e.lengthComputable) {
                const percentComplete = (e.loaded / e.total) * 100;
                progressFill.style.width = percentComplete + '%';
            }
        });

        xhr.addEventListener('load', () => {
            if (xhr.status === 201) {
                const response = JSON.parse(xhr.responseText);
                showToast(`${file.name} uploaded to FileStore successfully`, 'success');
                uploadStatus.innerHTML = `<div class="success-message">✅ ${file.name} upload completed</div>`;

                setTimeout(() => {
                    loadStores();
                    uploadProgress.style.display = 'none';
                    uploadStatus.innerHTML = '';
                }, 2000);
            } else {
                const error = JSON.parse(xhr.responseText);
                showToast(`Upload failed: ${error.error || 'Unknown error'}`, 'error');
                uploadStatus.innerHTML = `<div class="error-message">❌ Upload failed: ${error.error}</div>`;
            }
        });

        xhr.addEventListener('error', () => {
            showToast('An error occurred during upload', 'error');
            uploadStatus.innerHTML = '<div class="error-message">❌ Upload error</div>';
        });

        xhr.open('POST', '/api/stores/upload');
        xhr.send(formData);

    } catch (error) {
        showToast(`Error: ${error.message}`, 'error');
        uploadStatus.innerHTML = `<div class="error-message">❌ Error: ${error.message}</div>`;
    }
}

// ============================================================================
// Move Files to FileStore
// ============================================================================
let selectedFileForImport = null;

function showImportPanel(fileId, fileName) {
    selectedFileForImport = {
        file_id: fileId,
        display_name: fileName
    };

    const importPanel = document.getElementById('importPanel');
    importPanel.style.display = 'block';

    const storeSelect = document.getElementById('storeSelectForImport');
    storeSelect.innerHTML = '<option value="">Select FileStore...</option>';

    state.stores.forEach(store => {
        const option = document.createElement('option');
        option.value = store.store_name;
        option.textContent = store.display_name;
        storeSelect.appendChild(option);
    });
}

function cancelImportPanel() {
    document.getElementById('importPanel').style.display = 'none';
    selectedFileForImport = null;
}

async function confirmImportFile() {
    if (!selectedFileForImport) {
        showToast('No file selected', 'error');
        return;
    }

    const storeName = document.getElementById('storeSelectForImport').value;
    if (!storeName) {
        showToast('Please select a FileStore', 'error');
        return;
    }

    const importStatus = document.getElementById('importStatus');
    importStatus.innerHTML = '<div class="loading" style="display: flex; align-items: center; gap: 10px;"><div class="spinner"></div><span>Moving file...</span></div>';

    try {
        const response = await fetch('/api/files/import', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                file_id: selectedFileForImport.file_id,
                store_name: storeName,
                original_filename: selectedFileForImport.display_name
            })
        });

        const data = await response.json();

        if (data.success) {
            showToast(`${selectedFileForImport.display_name} moved to FileStore successfully`, 'success');
            importStatus.innerHTML = `<div class="success-message">✅ Move completed</div>`;

            setTimeout(() => {
                document.getElementById('importPanel').style.display = 'none';
                loadStores();
                selectedFileForImport = null;
            }, 2000);
        } else {
            showToast(`Move failed: ${data.error || 'Unknown error'}`, 'error');
            importStatus.innerHTML = `<div class="error-message">❌ Failed: ${data.error}</div>`;
        }
    } catch (error) {
        showToast(`Error: ${error.message}`, 'error');
        importStatus.innerHTML = `<div class="error-message">❌ Error: ${error.message}</div>`;
    }
}

// ============================================================================
// View FileStore Documents
// ============================================================================
async function showStoreDocuments(storeName, displayName) {
    const storesContainer = document.getElementById('storesList');

    try {
        const response = await fetch(`/api/stores/${encodeURIComponent(storeName)}/documents`);
        const data = await response.json();

        if (data.success) {
            const documents = data.documents || [];
            const documentCount = data.count || 0;

            const fileCountElement = document.querySelector(`.file-count-${storeName.replace(/\//g, '-')}`);
            if (fileCountElement) {
                fileCountElement.textContent = `${documentCount}`;
            }

            const documentListHtml = documents.length > 0
                ? `
                    <div class="store-documents">
                        <div class="documents-header">
                            <h4>Stored Documents (${documentCount})</h4>
                            <button class="btn btn-danger" onclick="deleteAllDocuments('${storeName}', '${displayName}')">Delete All</button>
                        </div>
                        <ul class="document-list">
                            ${documents.map((doc, index) => {
                                // Extract file extension from mime_type for better display
                                const mimeType = doc.mime_type || 'Unknown';
                                const fileExt = mimeType.split('/').pop().toUpperCase();

                                // Format file size
                                const sizeInMB = doc.size_bytes ? (doc.size_bytes / (1024 * 1024)).toFixed(2) + ' MB' : 'Unknown size';

                                // Format date
                                const createDate = doc.create_time ? new Date(doc.create_time).toLocaleDateString('ko-KR') : '';

                                // Display name with fallback
                                const displayName = doc.display_name || `Document ${index + 1}`;

                                return `
                                    <li class="document-item">
                                        <div class="doc-info">
                                            <span class="doc-name" title="${doc.document_name}">${displayName}</span>
                                            <div class="doc-details">
                                                <span class="doc-type">${fileExt}</span>
                                                <span class="doc-size">${sizeInMB}</span>
                                                ${createDate ? `<span class="doc-date">${createDate}</span>` : ''}
                                            </div>
                                        </div>
                                        <div class="doc-actions">
                                            <button class="btn btn-danger btn-sm" onclick="deleteDocument('${doc.document_name}', '${displayName}', '${storeName}', '${displayName}')">Delete</button>
                                        </div>
                                    </li>
                                `;
                            }).join('')}
                        </ul>
                    </div>
                `
                : '<p class="empty-message">No stored documents</p>';

            storesContainer.innerHTML = `
                <div class="store-detail-view">
                    <button class="btn btn-secondary" onclick="loadStores()">← Back</button>
                    <h3>${displayName}</h3>
                    ${documentListHtml}
                </div>
            `;

            showToast(`Loaded documents for ${displayName}`, 'success');
        } else {
            showToast(`Failed to load documents: ${data.error}`, 'error');
        }
    } catch (error) {
        showToast(`Error: ${error.message}`, 'error');
    }
}

async function deleteDocument(documentName, displayName, storeName, storeDisplayName) {
    if (!confirm(`Delete "${displayName}" from ${storeDisplayName}?\n\nNote: This will delete the document from the FileStore, but the original file in "My Files" (if it exists) will be preserved.`)) {
        return;
    }

    try {
        const response = await fetch(`/api/documents/${encodeURIComponent(documentName)}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (data.success) {
            showToast(`${displayName} deleted successfully`, 'success');
            // Refresh the document list for this store
            showStoreDocuments(storeName, storeDisplayName);
            // Also refresh the stores list to update counts
            setTimeout(() => loadStores(), 1000);
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        showToast(`Delete failed: ${error.message}`, 'error');
    }
}

async function deleteAllDocuments(storeName, storeDisplayName) {
    if (!confirm(`⚠️ WARNING: Delete ALL documents from "${storeDisplayName}"?\n\nThis will permanently delete ALL documents in this FileStore.\nThis action cannot be undone!\n\nNote: Original files in "My Files" (if they exist) will be preserved.`)) {
        return;
    }

    // Double confirmation for safety
    if (!confirm(`Are you absolutely sure?\n\nThis will delete ALL documents from "${storeDisplayName}".`)) {
        return;
    }

    try {
        showToast('Deleting all documents... This may take a while.', 'info');

        const response = await fetch(`/api/stores/${encodeURIComponent(storeName)}/documents`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (data.success) {
            const message = `Successfully deleted ${data.deleted_count} out of ${data.total_count} documents`;
            showToast(message, 'success');

            if (data.failed_count > 0) {
                console.error('Failed deletions:', data.errors);
                showToast(`Warning: ${data.failed_count} documents failed to delete. Check console for details.`, 'warning');
            }

            // Refresh the document list and stores list
            showStoreDocuments(storeName, storeDisplayName);
            setTimeout(() => loadStores(), 1000);
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        showToast(`Delete all failed: ${error.message}`, 'error');
    }
}

// ============================================================================
// Utilities
// ============================================================================
function showToast(message, type = 'info') {
    toast.textContent = message;
    toast.className = `toast show ${type}`;

    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}

// ============================================================================
// Multi-language Support
// ============================================================================
function changeLanguage(lang) {
    if (!translations[lang]) {
        console.error(`Language ${lang} not found`);
        return;
    }

    state.currentLanguage = lang;

    // Update all elements with data-i18n attributes
    document.querySelectorAll('[data-i18n]').forEach(element => {
        const key = element.getAttribute('data-i18n');
        if (translations[lang][key]) {
            // Handle different element types
            if (element.tagName === 'INPUT' || element.tagName === 'TEXTAREA') {
                element.placeholder = translations[lang][key];
            } else {
                element.textContent = translations[lang][key];
            }
        }
    });

    // Save language preference
    localStorage.setItem('preferredLanguage', lang);
}

// Load saved language preference
function loadLanguagePreference() {
    const savedLang = localStorage.getItem('preferredLanguage') || 'ko';
    const languageSelect = document.getElementById('languageSelect');

    if (languageSelect) {
        languageSelect.value = savedLang;
        changeLanguage(savedLang);
    }
}

// Setup language selector
document.addEventListener('DOMContentLoaded', () => {
    const languageSelect = document.getElementById('languageSelect');

    if (languageSelect) {
        languageSelect.addEventListener('change', (e) => {
            changeLanguage(e.target.value);
        });

        // Load saved preference on page load
        loadLanguagePreference();
    }
});

// ============================================================================
// Wayfinding (길찾기) Functions - Map Click Based
// ============================================================================

// Map click state
let mapClickState = {
    startCoords: null,
    endCoords: null,
    mode: 'wayfinding' // 'wayfinding' or 'facility'
};

// DOM 요소
const pathResult = document.getElementById('pathResult');
const pathLoading = document.getElementById('pathLoading');
const pathImage = document.getElementById('pathImage');
const pathDistance = document.getElementById('pathDistance');
const closePathResultBtn = document.getElementById('closePathResultBtn');
const resetMapBtn = document.getElementById('resetMapBtn');
const mapClickStatus = document.getElementById('mapClickStatus');
const initialMap = document.getElementById('initialMap');
const initialMapImage = document.getElementById('initialMapImage');

// Nearest Facility DOM 요소
const facilityPathResult = document.getElementById('facilityPathResult');
const facilityPathLoading = document.getElementById('facilityPathLoading');
const facilityPathImage = document.getElementById('facilityPathImage');
const facilityPathDistance = document.getElementById('facilityPathDistance');
const closeFacilityPathResultBtn = document.getElementById('closeFacilityPathResultBtn');
const resetFacilityMapBtn = document.getElementById('resetFacilityMapBtn');
const facilityMapStatus = document.getElementById('facilityMapStatus');
const facilityType = document.getElementById('facilityType');
const initialFacilityMap = document.getElementById('initialFacilityMap');
const initialFacilityMapImage = document.getElementById('initialFacilityMapImage');

// 이벤트 리스너 등록
if (closePathResultBtn) {
    closePathResultBtn.addEventListener('click', () => {
        pathResult.style.display = 'none';
    });
}

if (closeFacilityPathResultBtn) {
    closeFacilityPathResultBtn.addEventListener('click', () => {
        facilityPathResult.style.display = 'none';
    });
}

if (resetMapBtn) {
    resetMapBtn.addEventListener('click', resetMapClickState);
}

if (resetFacilityMapBtn) {
    resetFacilityMapBtn.addEventListener('click', resetFacilityMapClickState);
}

// 지도 초기화 (Wayfinding)
function resetMapClickState() {
    mapClickState.startCoords = null;
    mapClickState.endCoords = null;
    const lang = state.currentLanguage || 'ko';
    mapClickStatus.textContent = translations[lang]['click_start'];
    mapClickStatus.style.color = 'var(--text-secondary)';
    pathResult.style.display = 'none';
    if (initialMap) initialMap.style.display = 'block';
}

// 지도 초기화 (Facility)
function resetFacilityMapClickState() {
    mapClickState.startCoords = null;
    const lang = state.currentLanguage || 'ko';
    facilityMapStatus.textContent = translations[lang]['click_location'];
    facilityMapStatus.style.color = 'var(--text-secondary)';
    facilityPathResult.style.display = 'none';
    if (initialFacilityMap) initialFacilityMap.style.display = 'block';
}

// 지도 클릭 핸들러 (Wayfinding)
async function handleMapClick(event) {
    const rect = event.target.getBoundingClientRect();
    const x = event.clientX - rect.left;
    const y = event.clientY - rect.top;

    // 이미지 크기에 대한 실제 좌표 계산
    const scaleX = 953 / rect.width;
    const scaleY = 676 / rect.height;
    const actualX = x * scaleX;
    const actualY = y * scaleY;

    const lang = state.currentLanguage || 'ko';

    if (mapClickState.mode === 'wayfinding') {
        if (!mapClickState.startCoords) {
            // 출발지 설정
            mapClickState.startCoords = { x: actualX, y: actualY };
            mapClickStatus.textContent = translations[lang]['click_destination'];
            mapClickStatus.style.color = 'var(--success-color)';
        } else if (!mapClickState.endCoords) {
            // 도착지 설정 및 경로 찾기
            mapClickState.endCoords = { x: actualX, y: actualY };
            mapClickStatus.textContent = translations[lang]['calculating'];
            await findPathFromCoords();
        }
    } else if (mapClickState.mode === 'facility') {
        // 현재 위치에서 가장 가까운 시설물 찾기
        facilityMapStatus.textContent = translations[lang]['finding_facility'];
        await findNearestFacility(actualX, actualY);
    }
}

// 좌표 기반 경로 찾기
async function findPathFromCoords() {
    if (!mapClickState.startCoords || !mapClickState.endCoords) return;

    pathResult.style.display = 'none';
    pathLoading.style.display = 'flex';

    try {
        const response = await fetch('/api/wayfinding/find-path-coords', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                start_x: mapClickState.startCoords.x,
                start_y: mapClickState.startCoords.y,
                end_x: mapClickState.endCoords.x,
                end_y: mapClickState.endCoords.y
            })
        });

        const data = await response.json();
        pathLoading.style.display = 'none';

        const lang = state.currentLanguage || 'ko';

        if (data.success) {
            pathDistance.textContent = `${data.distance.toFixed(2)} km`;
            pathImage.src = `data:image/png;base64,${data.image}`;

            // 초기 지도 숨기고 결과 표시
            if (initialMap) initialMap.style.display = 'none';
            pathResult.style.display = 'block';

            mapClickStatus.textContent = translations[lang]['path_found'];
            mapClickStatus.style.color = 'var(--success-color)';

            showToast(translations[lang]['path_found'], 'success');
        } else {
            mapClickStatus.textContent = `실패: ${data.message}`;
            mapClickStatus.style.color = 'var(--danger-color)';
            showToast(`경로 찾기 실패: ${data.message || data.error}`, 'error');
            resetMapClickState();
        }
    } catch (error) {
        pathLoading.style.display = 'none';
        console.error('Error finding path:', error);
        mapClickStatus.textContent = '오류가 발생했습니다. 다시 시도해주세요.';
        mapClickStatus.style.color = 'var(--danger-color)';
        showToast('경로를 찾는 중 오류가 발생했습니다', 'error');
        resetMapClickState();
    }
}

// 시설물 타입에 따른 검색 패턴 매핑
const facilityPatterns = {
    'toilet': { category: 'toilet', name_pattern: null },
    'store': { category: 'others', name_pattern: '매점' },
    'water': { category: 'others', name_pattern: '음수대' },
    'parking': { category: 'others', name_pattern: '주차 사전무인정산기' }
};

// 가장 가까운 시설물 찾기
async function findNearestFacility(x, y) {
    facilityPathResult.style.display = 'none';
    facilityPathLoading.style.display = 'flex';

    try {
        const selectedType = facilityType.value;
        const searchParams = facilityPatterns[selectedType] || { category: 'toilet', name_pattern: null };

        const response = await fetch('/api/wayfinding/nearest-facility', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                x: x,
                y: y,
                category: searchParams.category,
                name_pattern: searchParams.name_pattern
            })
        });

        const data = await response.json();
        facilityPathLoading.style.display = 'none';

        const lang = state.currentLanguage || 'ko';

        if (data.success) {
            facilityPathDistance.textContent = `${data.distance.toFixed(2)} km`;
            facilityPathImage.src = `data:image/png;base64,${data.image}`;

            // 초기 지도 숨기고 결과 표시
            if (initialFacilityMap) initialFacilityMap.style.display = 'none';
            facilityPathResult.style.display = 'block';

            facilityMapStatus.textContent = translations[lang]['facility_found'];
            facilityMapStatus.style.color = 'var(--success-color)';

            showToast(translations[lang]['facility_found'], 'success');

            // 지도 클릭 핸들러 추가 (결과 이미지에)
            if (facilityPathImage) {
                facilityPathImage.addEventListener('click', handleMapClick);
            }
        } else {
            facilityMapStatus.textContent = `실패: ${data.message}`;
            facilityMapStatus.style.color = 'var(--danger-color)';
            showToast(`시설물 찾기 실패: ${data.message || data.error}`, 'error');
            resetFacilityMapClickState();
        }
    } catch (error) {
        facilityPathLoading.style.display = 'none';
        console.error('Error finding nearest facility:', error);
        facilityMapStatus.textContent = '오류가 발생했습니다. 다시 시도해주세요.';
        facilityMapStatus.style.color = 'var(--danger-color)';
        showToast('시설물을 찾는 중 오류가 발생했습니다', 'error');
        resetFacilityMapClickState();
    }
}

// 탭 전환 시 모드 설정 및 이미지 클릭 이벤트 추가
const originalHandleTabChange = handleTabChange;
handleTabChange = function(e) {
    originalHandleTabChange(e);

    const tabName = e.currentTarget.getAttribute('data-tab');

    if (tabName === 'wayfinding') {
        mapClickState.mode = 'wayfinding';
        resetMapClickState();

        // 초기 지도 및 결과 지도 이미지에 클릭 이벤트 추가
        setTimeout(() => {
            if (initialMapImage) {
                initialMapImage.addEventListener('click', handleMapClick);
            }
            if (pathImage) {
                pathImage.addEventListener('click', handleMapClick);
            }
        }, 100);
    } else if (tabName === 'facility') {
        mapClickState.mode = 'facility';
        resetFacilityMapClickState();

        // 초기 지도 및 결과 지도 이미지에 클릭 이벤트 추가
        setTimeout(() => {
            if (initialFacilityMapImage) {
                initialFacilityMapImage.addEventListener('click', handleMapClick);
            }
            if (facilityPathImage) {
                facilityPathImage.addEventListener('click', handleMapClick);
            }
        }, 100);
    }
};
