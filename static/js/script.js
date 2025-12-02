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
const deleteAllFilesBtn = document.getElementById('deleteAllFilesBtn');
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

    if (deleteAllFilesBtn) {
        deleteAllFilesBtn.addEventListener('click', deleteAllFiles);
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

    // Active store configuration
    const setActiveStoreBtn = document.getElementById('setActiveStoreBtn');
    if (setActiveStoreBtn) {
        setActiveStoreBtn.addEventListener('click', setActiveStore);
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
                <div class="status-message">임시 저장소에 업로드 완료</div>
            </div>
        `;
        showToast(`${fileName} 임시 저장소에 업로드 완료`, 'success');

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
                    <p>파일 로드 실패: ${error.message}</p>
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
                <p>업로드된 파일이 없습니다</p>
            </div>
        `;
        return;
    }

    filesList.innerHTML = state.files.map(file => {
        const sizeInMB = (file.size_bytes / (1024 * 1024)).toFixed(2);
        const fileName = file.display_name;
        const date = new Date(file.create_time).toLocaleDateString('ko-KR');
        const fileId = file.file_id;

        return `
            <div class="file-card">
                <div class="file-card-header">
                    <div class="file-icon">${getFileIcon(fileName)}</div>
                    <div class="file-card-actions">
                        <button title="파일 저장소로 이동" onclick="showImportPanel('${fileId}', '${fileName}')">📤</button>
                        <button title="삭제" onclick="deleteFile('${fileId}', '${fileName}')">🗑️</button>
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
    if (!confirm(`"${fileName}" 파일을 삭제하시겠습니까?`)) {
        return;
    }

    try {
        const response = await fetch(`/api/files/${fileId}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (data.success) {
            showToast(`${fileName} 삭제 완료`, 'success');
            loadFiles();
            loadStores();
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        showToast(`삭제 실패: ${error.message}`, 'error');
    }
}

async function deleteAllFiles() {
    if (!confirm(`⚠️ 경고: 임시 저장소의 모든 파일을 삭제하시겠습니까?\n\n이 작업은 되돌릴 수 없습니다!`)) {
        return;
    }

    // 이중 확인
    if (!confirm(`정말로 모든 파일을 삭제하시겠습니까?`)) {
        return;
    }

    try {
        showToast('모든 파일 삭제 중...', 'info');

        const response = await fetch('/api/files/delete-all', {
            method: 'DELETE'
        });

        const data = await response.json();

        if (data.success) {
            const message = `${data.deleted_count}개 파일 삭제 완료`;
            showToast(message, 'success');

            if (data.failed_count > 0) {
                console.error('삭제 실패:', data.errors);
                showToast(`경고: ${data.failed_count}개 파일 삭제 실패. 콘솔 확인 필요.`, 'warning');
            }

            loadFiles();
            loadStores();
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        showToast(`전체 삭제 실패: ${error.message}`, 'error');
    }
}

// File preview
async function previewFile(fileId, fileName) {
    try {
        const cleanFileId = fileId.replace(/^files\//, '');
        const response = await fetch(`/api/files/${cleanFileId}/preview`);
        const data = await response.json();

        if (!data.success) {
            showToast(`미리보기 불가: ${data.error}`, 'error');
            return;
        }

        // Files API files cannot be accessed directly in browser
        // Show file information instead
        const sizeInMB = (data.size_bytes / 1024 / 1024).toFixed(2);
        const createTime = data.create_time ? new Date(data.create_time).toLocaleString('ko-KR') : '알 수 없음';

        alert(
            `파일 정보:\n\n` +
            `이름: ${fileName}\n` +
            `타입: ${data.mime_type || '알 수 없음'}\n` +
            `크기: ${sizeInMB} MB\n` +
            `생성일: ${createTime}\n\n` +
            `참고: 임시 저장소의 파일은 직접 미리보기할 수 없습니다.\n` +
            `검색에 사용하려면 파일 저장소로 이동하세요.`
        );

        showToast(`${fileName} 정보 표시`, 'info');
    } catch (error) {
        showToast(`미리보기 오류: ${error.message}`, 'error');
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
            loadActiveStore();
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
                    <p>저장소 로드 실패: ${error.message}</p>
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
        storeSelect.innerHTML = '<option value="">파일 저장소 선택...</option>';

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
        storeSelectForUpload.innerHTML = '<option value="">파일 저장소 선택...</option>';

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

    // Update active store checkboxes
    const activeStoreCheckboxes = document.getElementById('activeStoreCheckboxes');
    if (activeStoreCheckboxes && state.stores.length > 0) {
        activeStoreCheckboxes.innerHTML = state.stores.map(store => `
            <label style="display: flex; align-items: center; padding: 8px; cursor: pointer; border-radius: 4px; margin-bottom: 4px; transition: background 0.2s;">
                <input type="checkbox" value="${store.store_name}" class="active-store-checkbox" style="margin-right: 10px; width: 18px; height: 18px; cursor: pointer;">
                <span style="flex: 1; font-weight: 500;">${store.display_name}</span>
                <span style="font-size: 12px; color: #666;">${store.active_documents_count || 0} 문서</span>
            </label>
        `).join('');

        // Add hover effect
        activeStoreCheckboxes.querySelectorAll('label').forEach(label => {
            label.addEventListener('mouseenter', () => {
                label.style.background = '#f0f0f0';
            });
            label.addEventListener('mouseleave', () => {
                label.style.background = 'transparent';
            });
        });
    }

    // Update import panel store select
    const storeSelectForImport = document.getElementById('storeSelectForImport');
    if (storeSelectForImport) {
        const selectedValue = storeSelectForImport.value;
        storeSelectForImport.innerHTML = '<option value="">파일 저장소 선택...</option>';

        state.stores.forEach(store => {
            const option = document.createElement('option');
            option.value = store.store_name;
            option.textContent = store.display_name;
            storeSelectForImport.appendChild(option);
        });

        if (selectedValue) {
            storeSelectForImport.value = selectedValue;
        }
    }
}

function renderStores() {
    const storesContainer = document.getElementById('storesList');
    if (!storesContainer) return;

    if (state.stores.length === 0) {
        storesContainer.innerHTML = `
            <div class="create-store-form">
                <h3>새 파일 저장소 만들기</h3>
                <input type="text" id="newStoreName" placeholder="저장소 이름 (예: 문서 저장소)" class="input-field">
                <button class="btn btn-primary" onclick="createStore()">만들기</button>
            </div>
            <div class="empty-state">
                <div class="empty-icon">💾</div>
                <p>생성된 파일 저장소가 없습니다</p>
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
        const createdDate = new Date(store.create_time).toLocaleDateString('ko-KR');

        return `
            <div class="store-card" onclick="showStoreDocuments('${store.store_name}', '${store.display_name}')">
                <div class="store-header">
                    <h3>${store.display_name}</h3>
                    <button class="btn btn-danger btn-sm" onclick="event.stopPropagation(); deleteStore('${store.store_name}', '${store.display_name}')" style="opacity: 0.85;">삭제</button>
                </div>
                <div class="store-info">
                    <div class="store-stat">
                        <span class="store-label">활성 문서:</span>
                        <span class="store-value file-count-${store.store_name.replace(/\//g, '-')}">${activeCount}</span>
                    </div>
                    <div class="store-stat">
                        <span class="store-label">처리 중:</span>
                        <span class="store-value">${pendingCount}</span>
                    </div>
                    ${failedCount > 0 ? `
                    <div class="store-stat">
                        <span class="store-label">실패:</span>
                        <span class="store-value error">${failedCount}</span>
                    </div>
                    ` : ''}
                    <div class="store-stat">
                        <span class="store-label">저장 용량:</span>
                        <span class="store-value">${sizeInMB} MB</span>
                    </div>
                    <div class="store-stat">
                        <span class="store-label">생성일:</span>
                        <span class="store-value">${createdDate}</span>
                    </div>
                    <div class="store-stat">
                        <span class="store-label">저장소 ID:</span>
                        <span class="store-value store-id" style="font-size: 12px;">${store.store_name}</span>
                    </div>
                </div>
            </div>
        `;
    }).join('');

    storesContainer.innerHTML = `
        <div class="create-store-form">
            <h3>새 파일 저장소 만들기</h3>
            <input type="text" id="newStoreName" placeholder="저장소 이름 (예: 문서 저장소)" class="input-field">
            <button class="btn btn-primary" onclick="createStore()">만들기</button>
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
        showToast('저장소 이름을 입력하세요', 'warning');
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
            showToast(`파일 저장소 "${name}" 생성 완료`, 'success');
            nameInput.value = '';
            loadStores();
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        showToast(`저장소 생성 실패: ${error.message}`, 'error');
    }
}

async function deleteStore(storeId, storeName) {
    if (!confirm(`파일 저장소 "${storeName}"를 삭제하시겠습니까?\n파일은 보존됩니다.`)) {
        return;
    }

    try {
        const response = await fetch(`/api/stores/${storeId}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (data.success) {
            showToast(`파일 저장소 "${storeName}" 삭제 완료`, 'success');
            loadStores();
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        showToast(`저장소 삭제 실패: ${error.message}`, 'error');
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
                <p>사용 가능한 파일 저장소가 없습니다</p>
                <small>파일 저장소 탭에서 저장소를 만드세요</small>
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
                <span class="checkbox-size">${fileCount} 문서</span>
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
    showToast('하나의 저장소만 선택할 수 있습니다', 'info');
}

async function performSearch() {
    // Check if required elements exist
    if (!searchQuery || !searchLoading || !chatHistory) {
        console.error('Required search elements not found');
        return;
    }

    const query = searchQuery.value.trim();
    if (!query) {
        showToast('검색할 질문을 입력하세요', 'warning');
        return;
    }

    // Add user message to UI immediately
    addMessageToChat('user', query);
    searchQuery.value = '';
    searchLoading.style.display = 'flex';

    try {
        const requestData = {
            query: query,
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

            showToast('검색 완료', 'success');
        } else {
            console.error('Search failed:', data.error);
            throw new Error(data.error);
        }
    } catch (error) {
        console.error('Search error:', error);
        showToast(`검색 실패: ${error.message}`, 'error');
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
    if (!confirm('모든 대화 내역을 지우시겠습니까?')) {
        return;
    }

    state.conversationHistory = [];

    if (chatHistory) {
        chatHistory.innerHTML = `
            <div class="empty-chat">
                <p>아직 대화가 없습니다. 질문을 시작해보세요!</p>
            </div>
        `;
    }

    showToast('대화 내역 삭제 완료', 'success');
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
            showToast('먼저 파일 저장소를 선택하세요', 'error');
            return;
        }

        const category = document.getElementById('categorySelectForUpload').value;

        Array.from(files).forEach(file => {
            uploadToFileSearchStore(file, store, category);
        });
    }
}

function handleFileSelectForStore(e) {
    const store = document.getElementById('storeSelectForUpload').value;
    if (!store) {
        showToast('먼저 파일 저장소를 선택하세요', 'error');
        return;
    }

    const category = document.getElementById('categorySelectForUpload').value;

    Array.from(e.target.files).forEach(file => {
        uploadToFileSearchStore(file, store, category);
    });
}

async function uploadToFileSearchStore(file, storeName, category) {
    const validExtensions = ['pdf', 'txt', 'doc', 'docx', 'xlsx', 'xls', 'ppt', 'pptx', 'csv', 'json', 'xml', 'html'];
    const ext = file.name.split('.').pop().toLowerCase();

    if (!validExtensions.includes(ext)) {
        showToast(`지원하지 않는 파일 형식: ${file.name}`, 'error');
        return;
    }

    const uploadProgress = document.getElementById('uploadToStoreProgress');
    const uploadStatus = document.getElementById('uploadToStoreStatus');
    const progressFill = document.getElementById('progressFillStore');
    const uploadFileName = document.getElementById('uploadToStoreFileName');

    uploadFileName.textContent = `${file.name} 업로드 중...`;
    uploadProgress.style.display = 'block';
    uploadStatus.innerHTML = '';

    try {
        const formData = new FormData();
        formData.append('file', file);
        formData.append('store_name', storeName);
        if (category) {
            formData.append('category', category);
        }

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
                showToast(`${file.name} 파일 저장소에 업로드 완료`, 'success');
                uploadStatus.innerHTML = `<div class="success-message">✅ ${file.name} 업로드 완료</div>`;

                setTimeout(() => {
                    loadStores();
                    uploadProgress.style.display = 'none';
                    uploadStatus.innerHTML = '';
                }, 2000);
            } else {
                const error = JSON.parse(xhr.responseText);
                showToast(`업로드 실패: ${error.error || '알 수 없는 오류'}`, 'error');
                uploadStatus.innerHTML = `<div class="error-message">❌ 업로드 실패: ${error.error}</div>`;
            }
        });

        xhr.addEventListener('error', () => {
            showToast('업로드 중 오류 발생', 'error');
            uploadStatus.innerHTML = '<div class="error-message">❌ 업로드 오류</div>';
        });

        xhr.open('POST', '/api/stores/upload');
        xhr.send(formData);

    } catch (error) {
        showToast(`오류: ${error.message}`, 'error');
        uploadStatus.innerHTML = `<div class="error-message">❌ 오류: ${error.message}</div>`;
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
    storeSelect.innerHTML = '<option value="">파일 저장소 선택...</option>';

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
        showToast('선택된 파일이 없습니다', 'error');
        return;
    }

    const storeName = document.getElementById('storeSelectForImport').value;
    if (!storeName) {
        showToast('파일 저장소를 선택하세요', 'error');
        return;
    }

    const category = document.getElementById('categorySelectForImport').value;

    const importStatus = document.getElementById('importStatus');
    importStatus.innerHTML = '<div class="loading" style="display: flex; align-items: center; gap: 10px;"><div class="spinner"></div><span>파일 이동 중...</span></div>';

    try {
        const response = await fetch('/api/files/import', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                file_id: selectedFileForImport.file_id,
                store_name: storeName,
                original_filename: selectedFileForImport.display_name,
                category: category || null
            })
        });

        const data = await response.json();

        if (data.success) {
            showToast(`${selectedFileForImport.display_name} 파일 저장소로 이동 완료`, 'success');
            importStatus.innerHTML = `<div class="success-message">✅ 이동 완료</div>`;

            setTimeout(() => {
                document.getElementById('importPanel').style.display = 'none';
                loadStores();
                selectedFileForImport = null;
            }, 2000);
        } else {
            showToast(`이동 실패: ${data.error || '알 수 없는 오류'}`, 'error');
            importStatus.innerHTML = `<div class="error-message">❌ 실패: ${data.error}</div>`;
        }
    } catch (error) {
        showToast(`오류: ${error.message}`, 'error');
        importStatus.innerHTML = `<div class="error-message">❌ 오류: ${error.message}</div>`;
    }
}

// ============================================================================
// View FileStore Documents
// ============================================================================
async function showStoreDocuments(storeName, displayName, selectedCategory = '') {
    const storesContainer = document.getElementById('storesList');

    try {
        const response = await fetch(`/api/stores/${encodeURIComponent(storeName)}/documents`);
        const data = await response.json();

        if (data.success) {
            const allDocuments = data.documents || [];
            const documentCount = data.count || 0;

            // Get unique categories
            const categories = [...new Set(allDocuments.map(doc => doc.category || '미분류'))].sort();

            // Filter documents by selected category
            const documents = selectedCategory ? allDocuments.filter(doc => (doc.category || '미분류') === selectedCategory) : allDocuments;
            const filteredCount = documents.length;

            const fileCountElement = document.querySelector(`.file-count-${storeName.replace(/\//g, '-')}`);
            if (fileCountElement) {
                fileCountElement.textContent = `${documentCount}`;
            }

            const documentListHtml = documents.length > 0
                ? `
                    <div class="store-documents">
                        <div class="documents-header">
                            <h4>문서 목록 (${selectedCategory ? `${filteredCount} / ${documentCount}` : documentCount})</h4>
                            <div style="display: flex; gap: 10px;">
                                ${selectedCategory ? `<button class="btn btn-danger" onclick="deleteDocumentsByCategory('${storeName}', '${displayName}', '${selectedCategory}')">선택된 카테고리 삭제 (${filteredCount})</button>` : ''}
                                <button class="btn btn-danger" onclick="deleteAllDocuments('${storeName}', '${displayName}')">전체 삭제</button>
                            </div>
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
                                const docDisplayName = doc.display_name || `Document ${index + 1}`;

                                // Category with fallback
                                const category = doc.category || '미분류';

                                return `
                                    <li class="document-item">
                                        <div class="doc-info">
                                            <span class="doc-name" title="${doc.document_name}">${docDisplayName}</span>
                                            <div class="doc-details">
                                                <span class="doc-type">${fileExt}</span>
                                                <span class="doc-size">${sizeInMB}</span>
                                                ${createDate ? `<span class="doc-date">${createDate}</span>` : ''}
                                                <span class="doc-category" style="background: #e9ecef; padding: 2px 8px; border-radius: 4px; font-size: 12px;">📂 ${category}</span>
                                            </div>
                                        </div>
                                        <div class="doc-actions">
                                            <button class="btn btn-danger btn-sm" onclick="deleteDocument('${doc.document_name}', '${docDisplayName}', '${storeName}', '${displayName}')">삭제</button>
                                        </div>
                                    </li>
                                `;
                            }).join('')}
                        </ul>
                    </div>
                `
                : '<p class="empty-message">문서가 없습니다</p>';

            storesContainer.innerHTML = `
                <div class="store-detail-view">
                    <button class="btn btn-secondary" onclick="loadStores()">← 뒤로</button>
                    <h3>${displayName}</h3>
                    ${categories.length > 0 ? `
                        <div style="margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 8px;">
                            <label style="display: block; margin-bottom: 8px; font-weight: 500;">📂 카테고리 필터:</label>
                            <select id="categoryFilter" class="input-field" onchange="showStoreDocuments('${storeName}', '${displayName}', this.value)" style="width: 100%; max-width: 400px;">
                                <option value="">전체 보기 (${documentCount})</option>
                                ${categories.map(cat => `
                                    <option value="${cat}" ${cat === selectedCategory ? 'selected' : ''}>
                                        ${cat} (${allDocuments.filter(d => (d.category || '미분류') === cat).length})
                                    </option>
                                `).join('')}
                            </select>
                        </div>
                    ` : ''}
                    ${documentListHtml}
                </div>
            `;

            showToast(`${displayName} 문서 로드 완료`, 'success');
        } else {
            showToast(`문서 로드 실패: ${data.error}`, 'error');
        }
    } catch (error) {
        showToast(`에러: ${error.message}`, 'error');
    }
}

async function deleteDocument(documentName, displayName, storeName, storeDisplayName) {
    if (!confirm(`"${displayName}"을(를) ${storeDisplayName}에서 삭제하시겠습니까?\n\n참고: 파일 저장소에서 문서가 삭제되지만, 임시 저장소의 원본 파일(있는 경우)은 보존됩니다.`)) {
        return;
    }

    try {
        const response = await fetch(`/api/documents/${encodeURIComponent(documentName)}`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (data.success) {
            showToast(`${displayName} 삭제 완료`, 'success');
            // Refresh the document list for this store
            showStoreDocuments(storeName, storeDisplayName);
            // Also refresh the stores list to update counts
            setTimeout(() => loadStores(), 1000);
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        showToast(`삭제 실패: ${error.message}`, 'error');
    }
}

async function deleteAllDocuments(storeName, storeDisplayName) {
    if (!confirm(`⚠️ 경고: "${storeDisplayName}"의 모든 문서를 삭제하시겠습니까?\n\n이 작업은 파일 저장소의 모든 문서를 영구적으로 삭제합니다.\n이 작업은 되돌릴 수 없습니다!\n\n참고: 임시 저장소의 원본 파일(있는 경우)은 보존됩니다.`)) {
        return;
    }

    // Double confirmation for safety
    if (!confirm(`정말로 확실하십니까?\n\n"${storeDisplayName}"의 모든 문서가 삭제됩니다.`)) {
        return;
    }

    try {
        showToast('모든 문서 삭제 중... 시간이 걸릴 수 있습니다.', 'info');

        const response = await fetch(`/api/stores/${encodeURIComponent(storeName)}/documents`, {
            method: 'DELETE'
        });

        const data = await response.json();

        if (data.success) {
            const message = `${data.total_count}개 중 ${data.deleted_count}개 문서 삭제 완료`;
            showToast(message, 'success');

            if (data.failed_count > 0) {
                console.error('Failed deletions:', data.errors);
                showToast(`경고: ${data.failed_count}개 문서 삭제 실패. 콘솔 확인 필요.`, 'warning');
            }

            // Refresh the document list and stores list
            showStoreDocuments(storeName, storeDisplayName);
            setTimeout(() => loadStores(), 1000);
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        showToast(`전체 삭제 실패: ${error.message}`, 'error');
    }
}

async function deleteDocumentsByCategory(storeName, storeDisplayName, category) {
    if (!confirm(`⚠️ 경고: "${category}" 카테고리의 모든 문서를 삭제하시겠습니까?\n\n이 작업은 되돌릴 수 없습니다!`)) {
        return;
    }

    try {
        showToast(`"${category}" 카테고리 문서 삭제 중...`, 'info');

        const response = await fetch(`/api/stores/${encodeURIComponent(storeName)}/documents/delete-by-category`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ category })
        });

        const data = await response.json();

        if (data.success) {
            const message = `${data.deleted_count}개 문서 삭제 완료`;
            showToast(message, 'success');

            if (data.failed_count > 0) {
                console.error('삭제 실패:', data.errors);
                showToast(`경고: ${data.failed_count}개 문서 삭제 실패. 콘솔 확인 필요.`, 'warning');
            }

            // Refresh the document list (clear category filter)
            showStoreDocuments(storeName, storeDisplayName);
            setTimeout(() => loadStores(), 1000);
        } else {
            throw new Error(data.error);
        }
    } catch (error) {
        showToast(`카테고리 삭제 실패: ${error.message}`, 'error');
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
        console.error(`언어 ${lang}을(를) 찾을 수 없습니다`);
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

// ============================================================================
// Active Store Configuration
// ============================================================================
async function loadActiveStore() {
    try {
        const response = await fetch('/api/config/active-stores');
        const data = await response.json();

        if (data.success && data.active_stores && data.active_stores.length > 0) {
            const activeStoreStatus = document.getElementById('activeStoreStatus');
            const currentActiveStores = document.getElementById('currentActiveStores');

            // Check the appropriate checkboxes
            document.querySelectorAll('.active-store-checkbox').forEach(checkbox => {
                checkbox.checked = data.active_stores.includes(checkbox.value);
            });

            if (activeStoreStatus && currentActiveStores) {
                const storeNames = data.active_stores.map(storeName => {
                    const store = state.stores.find(s => s.store_name === storeName);
                    return store ? store.display_name : storeName;
                });
                currentActiveStores.innerHTML = storeNames.map(name =>
                    `<div style="padding: 4px 8px; background: #007bff; color: white; border-radius: 4px; display: inline-block; margin: 2px; font-size: 13px;">✓ ${name}</div>`
                ).join('');
                activeStoreStatus.style.display = 'block';
            }
        } else {
            const activeStoreStatus = document.getElementById('activeStoreStatus');
            if (activeStoreStatus) {
                activeStoreStatus.style.display = 'none';
            }
            // Uncheck all checkboxes
            document.querySelectorAll('.active-store-checkbox').forEach(checkbox => {
                checkbox.checked = false;
            });
        }
    } catch (error) {
        console.error('Error loading active stores:', error);
    }
}

async function setActiveStore() {
    const checkboxes = document.querySelectorAll('.active-store-checkbox:checked');
    const storeNames = Array.from(checkboxes).map(cb => cb.value);

    if (storeNames.length === 0) {
        showToast('최소 하나의 파일 저장소를 선택하세요', 'warning');
        return;
    }

    try {
        const response = await fetch('/api/config/active-stores', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                store_names: storeNames
            })
        });

        const data = await response.json();

        if (data.success) {
            showToast(`${storeNames.length}개 활성 파일 저장소 설정 완료`, 'success');
            loadActiveStore();
        } else {
            showToast(`활성 저장소 설정 실패: ${data.error}`, 'error');
        }
    } catch (error) {
        console.error('Error setting active stores:', error);
        showToast(`오류: ${error.message}`, 'error');
    }
}
