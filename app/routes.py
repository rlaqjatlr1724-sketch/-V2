from flask import Blueprint, render_template, request, jsonify, current_app
from app.logger import get_logger
from werkzeug.utils import secure_filename
import os
import tempfile
from app.gemini_client import GeminiClient

bp = Blueprint('main', __name__)

# 허용되는 파일 확장자
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'doc', 'docx', 'xlsx', 'xls', 'ppt', 'pptx', 'csv', 'json', 'xml', 'html'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# ==================== Index Route ====================

@bp.route('/')
def index():
    logger = get_logger()
    logger.info(f'Index page request - IP: {request.remote_addr}')
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f'Index page rendering failed - IP: {request.remote_addr} - Error: {str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== FileSearchStore Management ====================

@bp.route('/api/stores/create', methods=['POST'])
def create_store():
    """새 FileSearchStore 생성"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'Store creation request - IP: {client_ip}')

        data = request.get_json()
        store_name = data.get('name', '').strip()

        if not store_name:
            logger.warning(f'Store name is missing - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'Store name is required'}), 400

        logger.debug(f'Store creation attempt - Name: {store_name} - IP: {client_ip}')

        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        result = gemini.create_file_search_store(store_name)

        if result['success']:
            logger.info(f'Store creation successful - Name: {store_name} - Store ID: {result.get("store_name")} - IP: {client_ip}')
            return jsonify(result), 201
        else:
            logger.error(f'Store creation failed - Name: {store_name} - Error: {result.get("error")} - IP: {client_ip}')
            return jsonify(result), 400

    except Exception as e:
        logger.error(f'Store creation exception occurred - IP: {client_ip} - Error: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/stores', methods=['GET'])
def list_stores():
    """모든 FileSearchStore 조회"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'Store list retrieval request - IP: {client_ip}')

        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        result = gemini.list_file_search_stores()

        if result['success']:
            store_count = result.get('count', 0)
            logger.info(f'Store list retrieval successful - Count: {store_count} - IP: {client_ip}')
            logger.debug(f'Retrieved stores: {result.get("stores")} - IP: {client_ip}')
            return jsonify(result), 200
        else:
            logger.error(f'Store list retrieval failed - Error: {result.get("error")} - IP: {client_ip}')
            return jsonify(result), 400

    except Exception as e:
        logger.error(f'Store list retrieval exception occurred - IP: {client_ip} - Error: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/stores/<path:store_id>', methods=['GET'])
def get_store(store_id):
    """특정 FileSearchStore 조회"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'Store retrieval request - Store ID: {store_id} - IP: {client_ip}')

        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        result = gemini.get_file_search_store(store_id)

        if result['success']:
            logger.info(f'Store retrieval successful - Store ID: {store_id} - IP: {client_ip}')
            logger.debug(f'Store information: {result} - IP: {client_ip}')
            return jsonify(result), 200
        else:
            logger.warning(f'Store retrieval failed - Store ID: {store_id} - Error: {result.get("error")} - IP: {client_ip}')
            return jsonify(result), 404

    except Exception as e:
        logger.error(f'Store retrieval exception occurred - IP: {client_ip} - Error: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/stores/<path:store_id>/documents', methods=['GET'])
def get_store_documents(store_id):
    """FileSearchStore의 문서 목록 조회"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'Store document list retrieval request - Store ID: {store_id} - IP: {client_ip}')

        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        result = gemini.list_documents_in_store(store_id)

        if result['success']:
            doc_count = result.get('count', 0)
            logger.info(f'Store document list retrieval successful - Store ID: {store_id} - Count: {doc_count} - IP: {client_ip}')
            logger.debug(f'Retrieved documents: {result.get("documents")} - IP: {client_ip}')
            return jsonify(result), 200
        else:
            logger.error(f'Store document list retrieval failed - Store ID: {store_id} - Error: {result.get("error")} - IP: {client_ip}')
            return jsonify(result), 400

    except Exception as e:
        logger.error(f'Store retrieval exception occurred - Store ID: {store_id} - IP: {client_ip} - Error: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/stores/<path:store_id>', methods=['DELETE'])
def delete_store(store_id):
    """FileSearchStore 삭제"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'Store deletion request - Store ID: {store_id} - IP: {client_ip}')

        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        result = gemini.delete_file_search_store(store_id)

        if result['success']:
            logger.info(f'Store deletion successful - Store ID: {store_id} - IP: {client_ip}')
            return jsonify(result), 200
        else:
            logger.error(f'Store deletion failed - Store ID: {store_id} - Error: {result.get("error")} - IP: {client_ip}')
            return jsonify(result), 400

    except Exception as e:
        logger.error(f'Store deletion exception occurred - Store ID: {store_id} - IP: {client_ip} - Error: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== File Management ====================

@bp.route('/api/files/upload', methods=['POST'])
def upload_file():
    """파일 업로드 (Files API)"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'File upload request - IP: {client_ip}')

        if 'file' not in request.files:
            logger.warning(f'File is missing - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            logger.warning(f'No filename - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            logger.warning(f'File type not allowed - Filename: {file.filename} - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'File type not allowed'}), 400

        logger.debug(f'File upload started - Filename: {file.filename} - IP: {client_ip}')

        # 임시 파일에 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name

        try:
            # Gemini Files API를 통해 파일 업로드
            gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
            result = gemini.upload_file(tmp_path)

            if result['success']:
                logger.info(f'File upload successful - Filename: {file.filename} - File ID: {result.get("file_id")} - IP: {client_ip}')
                logger.debug(f'Upload result: {result} - IP: {client_ip}')
                return jsonify(result), 201
            else:
                logger.error(f'File upload failed - Filename: {file.filename} - Error: {result.get("error")} - IP: {client_ip}')
                return jsonify(result), 400
        finally:
            # 임시 파일 삭제
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
                logger.debug(f'Temporary file deletion completed - Path: {tmp_path} - IP: {client_ip}')

    except Exception as e:
        logger.error(f'File upload exception occurred - IP: {client_ip} - Error: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/files/<path:file_id>/import', methods=['POST'])
def import_file(file_id):
    """파일을 FileSearchStore로 임포트"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'File import request - File ID: {file_id} - IP: {client_ip}')

        data = request.get_json()
        store_id = data.get('store_id', '').strip()
        metadata = data.get('metadata', None)

        if not store_id:
            logger.warning(f'Store ID is missing - File ID: {file_id} - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'store_id is required'}), 400

        logger.debug(f'File import attempt - File ID: {file_id} - Store ID: {store_id} - Metadata: {metadata} - IP: {client_ip}')

        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        result = gemini.import_file_to_store(file_id, store_id, metadata)

        if result['success']:
            logger.info(f'File import successful - File ID: {file_id} - Store ID: {store_id} - IP: {client_ip}')
            return jsonify(result), 200
        else:
            logger.error(f'File import failed - File ID: {file_id} - Store ID: {store_id} - Error: {result.get("error")} - IP: {client_ip}')
            return jsonify(result), 400

    except Exception as e:
        logger.error(f'File import exception occurred - File ID: {file_id} - IP: {client_ip} - Error: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/files', methods=['GET'])
def list_files():
    """모든 파일 조회"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'File list retrieval request - IP: {client_ip}')

        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        result = gemini.list_files()

        if result['success']:
            file_count = result.get('count', 0)
            logger.info(f'File list retrieval successful - Count: {file_count} - IP: {client_ip}')
            logger.debug(f'Retrieved files: {result.get("files")} - IP: {client_ip}')
            return jsonify(result), 200
        else:
            logger.error(f'File list retrieval failed - Error: {result.get("error")} - IP: {client_ip}')
            return jsonify(result), 400

    except Exception as e:
        logger.error(f'File list retrieval exception occurred - IP: {client_ip} - Error: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/files/<path:file_id>', methods=['GET'])
def get_file_info(file_id):
    """특정 파일 정보 조회"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'File information retrieval request - File ID: {file_id} - IP: {client_ip}')

        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        result = gemini.get_file(file_id)

        if result['success']:
            logger.info(f'File information retrieval successful - File ID: {file_id} - IP: {client_ip}')
            logger.debug(f'File information: {result} - IP: {client_ip}')
            return jsonify(result), 200
        else:
            logger.warning(f'File information retrieval failed - File ID: {file_id} - Error: {result.get("error")} - IP: {client_ip}')
            return jsonify(result), 404

    except Exception as e:
        logger.error(f'File information retrieval exception occurred - File ID: {file_id} - IP: {client_ip} - Error: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/files/<path:file_id>', methods=['DELETE'])
def delete_file(file_id):
    """파일 삭제"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'File deletion request - File ID: {file_id} - IP: {client_ip}')

        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        result = gemini.delete_file(file_id)

        if result['success']:
            logger.info(f'File deletion successful - File ID: {file_id} - IP: {client_ip}')
            return jsonify(result), 200
        else:
            logger.error(f'File deletion failed - File ID: {file_id} - Error: {result.get("error")} - IP: {client_ip}')
            return jsonify(result), 400

    except Exception as e:
        logger.error(f'File deletion exception occurred - File ID: {file_id} - IP: {client_ip} - Error: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== Search ====================

@bp.route('/api/search', methods=['POST'])
def search():
    """FileSearch로 검색"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'Search request - IP: {client_ip}')

        data = request.get_json()
        query = data.get('query', '').strip()
        store_ids = data.get('store_ids', [])
        metadata_filter = data.get('metadata_filter', None)

        if not query:
            logger.warning(f'Search query is missing - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'Query is required'}), 400

        if not store_ids:
            logger.warning(f'Store ID is missing - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'store_ids is required'}), 400

        if not isinstance(store_ids, list):
            logger.warning(f'Invalid store_ids format - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'store_ids must be an array'}), 400

        logger.debug(f'Search started - Query: {query} - Stores: {store_ids} - Metadata filter: {metadata_filter} - IP: {client_ip}')

        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        result = gemini.search_with_file_search(query, store_ids, metadata_filter)

        if result['success']:
            logger.info(f'Search successful - Query: {query} - Stores: {store_ids} - IP: {client_ip}')
            logger.debug(f'Search result length: {len(result.get("result", ""))} characters - IP: {client_ip}')
            return jsonify(result), 200
        else:
            logger.error(f'Search failed - Query: {query} - Error: {result.get("error")} - IP: {client_ip}')
            return jsonify(result), 400

    except Exception as e:
        logger.error(f'Search exception occurred - IP: {client_ip} - Error: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== File Preview Route ====================

@bp.route('/api/files/<path:file_id>/preview', methods=['GET'])
def preview_file(file_id):
    """파일 미리보기/다운로드"""
    logger = get_logger()
    client_ip = request.remote_addr
    
    # file_id에서 "files/" 제거 (중복 방지)
    if not file_id.startswith('files/'):
        file_id = f"files/{file_id}"
    
    logger.info(f'File preview request - File ID: {file_id}, IP: {client_ip}')
    try:
        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        file_info = gemini.get_file(file_id)
        
        if not file_info.get('success'):
            logger.warning(f'File retrieval failed - File ID: {file_id}')
            return jsonify({'success': False, 'error': 'File not found'}), 404
        
        # 파일 URI를 반환 (클라이언트에서 직접 접근 가능)
        file_uri = file_info.get('uri')
        if not file_uri:
            logger.warning(f'File URI not available - File ID: {file_id}')
            return jsonify({'success': False, 'error': 'File URI not available'}), 400
        
        logger.info(f'File preview information returned - File ID: {file_id}')
        return jsonify({
            'success': True,
            'file_id': file_id,
            'display_name': file_info.get('display_name'),
            'mime_type': file_info.get('mime_type'),
            'size_bytes': file_info.get('size_bytes'),
            'uri': file_uri
        }), 200
    except Exception as e:
        logger.error(f'File preview error occurred: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== FileStore Direct Upload ====================

@bp.route('/api/stores/upload', methods=['POST'])
def upload_to_store():
    """FileStore에 파일 직접 업로드 (uploadToFileSearchStore)"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'FileStore direct upload request - IP: {client_ip}')

        # 요청 데이터 검증
        if 'file' not in request.files:
            logger.warning(f'No file - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'No file provided'}), 400

        file = request.files['file']
        store_name = request.form.get('store_name', '').strip()

        if not file or not store_name:
            logger.warning(f'File or store name is missing - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'File and store name are required'}), 400

        if not allowed_file(file.filename):
            logger.warning(f'Unsupported file type - Filename: {file.filename} - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'File type not allowed'}), 400

        # 임시 파일에 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
            file.save(tmp_file.name)
            tmp_file_path = tmp_file.name

        try:
            logger.debug(f'FileStore upload attempt - File: {file.filename} - Store: {store_name} - IP: {client_ip}')

            gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
            result = gemini.upload_and_import_to_store(
                file_path=tmp_file_path,
                store_name=store_name,
                display_name=file.filename
            )

            if result['success']:
                logger.info(f'FileStore upload successful - File: {file.filename} - Store: {store_name} - IP: {client_ip}')
                return jsonify(result), 201
            else:
                logger.error(f'FileStore upload failed - File: {file.filename} - Error: {result.get("error")} - IP: {client_ip}')
                return jsonify(result), 400

        finally:
            # 임시 파일 삭제
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

    except Exception as e:
        logger.error(f'FileStore upload exception occurred - IP: {client_ip} - Error: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== File Import to Store ====================

@bp.route('/api/files/import', methods=['POST'])
def import_file_to_store():
    """Files API의 파일을 FileStore로 import"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'File import request - IP: {client_ip}')

        data = request.get_json()
        file_id = data.get('file_id', '').strip()
        store_name = data.get('store_name', '').strip()

        if not file_id or not store_name:
            logger.warning(f'File ID or store name is missing - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'File ID and store name are required'}), 400

        logger.debug(f'File import attempt - File: {file_id} - Store: {store_name} - IP: {client_ip}')

        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        result = gemini.import_file_to_store(
            file_id=file_id,
            store_name=store_name
        )

        if result['success']:
            logger.info(f'File import successful - File: {file_id} - Store: {store_name} - IP: {client_ip}')
            return jsonify(result), 201
        else:
            logger.error(f'File import failed - File: {file_id} - Error: {result.get("error")} - IP: {client_ip}')
            return jsonify(result), 400

    except Exception as e:
        logger.error(f'File import exception occurred - IP: {client_ip} - Error: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500
