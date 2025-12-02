from flask import Blueprint, render_template, request, jsonify, current_app
from app.logger import get_logger
from werkzeug.utils import secure_filename
import os
import tempfile
import csv
import json
import sqlite3
from app.gemini_client import GeminiClient
from app.wayfinding import WayfindingService
from app.db import set_config, get_config

bp = Blueprint('main', __name__)

# 길찾기 서비스 초기화
wayfinding_service = None

def get_wayfinding_service():
    """길찾기 서비스 싱글톤 인스턴스 반환"""
    global wayfinding_service
    if wayfinding_service is None:
        wayfinding_service = WayfindingService()
    return wayfinding_service

# 허용되는 파일 확장자
ALLOWED_EXTENSIONS = {'pdf', 'txt', 'doc', 'docx', 'xlsx', 'xls', 'ppt', 'pptx', 'csv', 'json', 'xml', 'html'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_csv_to_json(file_path, filename):
    """
    CSV 파일을 JSON으로 변환

    Args:
        file_path: CSV 파일 경로
        filename: 원본 파일 이름

    Returns:
        tuple: (변환된 JSON 파일 경로, 새 파일 이름)
    """
    logger = get_logger()

    # CSV 파일만 처리
    if not filename.lower().endswith('.csv'):
        return file_path, filename

    try:
        logger.info(f"Converting CSV to JSON: {filename}")

        # CSV 읽기 (여러 인코딩 시도)
        encodings = ['utf-8', 'cp949', 'euc-kr', 'latin-1']
        data = None

        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as csvfile:
                    reader = csv.DictReader(csvfile)
                    data = list(reader)
                logger.info(f"Successfully read CSV with {encoding} encoding")
                break
            except (UnicodeDecodeError, Exception) as e:
                logger.debug(f"Failed to read with {encoding}: {str(e)}")
                continue

        if data is None:
            logger.error(f"Failed to read CSV file with any encoding")
            return file_path, filename

        # JSON으로 변환하여 임시 파일에 저장
        json_filename = filename.rsplit('.', 1)[0] + '.json'
        with tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.json', encoding='utf-8') as tmp_file:
            json.dump(data, tmp_file, ensure_ascii=False, indent=2)
            new_path = tmp_file.name

        logger.info(f"Converted CSV to JSON: {json_filename} ({len(data)} rows)")
        return new_path, json_filename

    except Exception as e:
        logger.error(f"Error converting CSV to JSON: {str(e)}", exc_info=True)
        return file_path, filename

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

@bp.route('/admin')
def admin():
    logger = get_logger()
    logger.info(f'Admin page request - IP: {request.remote_addr}')
    try:
        return render_template('admin.html')
    except Exception as e:
        logger.error(f'Admin page rendering failed - IP: {request.remote_addr} - Error: {str(e)}')
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
        original_filename = file.filename  # 원본 파일명 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name

        converted_path = None
        try:
            # CSV 파일을 JSON으로 변환
            converted_path, converted_filename = convert_csv_to_json(tmp_path, original_filename)
            final_path = converted_path
            final_filename = converted_filename

            # Gemini Files API를 통해 파일 업로드 (변환된 파일명을 display_name으로 전달)
            gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
            result = gemini.upload_file(final_path, display_name=final_filename)

            if result['success']:
                logger.info(f'File upload successful - Original: {original_filename} - Uploaded as: {final_filename} - File ID: {result.get("file_id")} - IP: {client_ip}')
                logger.debug(f'Upload result: {result} - IP: {client_ip}')
                return jsonify(result), 201
            else:
                logger.error(f'File upload failed - Filename: {final_filename} - Error: {result.get("error")} - IP: {client_ip}')
                return jsonify(result), 400
        finally:
            # 임시 파일 삭제
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
                logger.debug(f'Temporary file deletion completed - Path: {tmp_path} - IP: {client_ip}')
            # 변환된 파일도 삭제 (원본과 다른 경우)
            if converted_path and converted_path != tmp_path and os.path.exists(converted_path):
                os.remove(converted_path)
                logger.debug(f'Converted file deletion completed - Path: {converted_path} - IP: {client_ip}')

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

@bp.route('/api/files/delete-all', methods=['DELETE'])
def delete_all_files():
    """임시 저장소의 모든 파일 삭제"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'Delete all files request - IP: {client_ip}')

        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])

        # 모든 파일 목록 조회
        files_result = gemini.list_files()

        if not files_result['success']:
            return jsonify({'success': False, 'error': 'Failed to list files'}), 400

        files = files_result.get('files', [])
        total_count = len(files)

        if total_count == 0:
            logger.info(f'No files to delete - IP: {client_ip}')
            return jsonify({
                'success': True,
                'message': 'No files to delete',
                'deleted_count': 0,
                'total_count': 0
            }), 200

        # 파일 삭제
        deleted_count = 0
        failed_count = 0
        errors = []

        for file in files:
            file_id = file.get('file_id')
            try:
                result = gemini.delete_file(file_id)
                if result['success']:
                    deleted_count += 1
                else:
                    failed_count += 1
                    errors.append(f"Failed to delete {file_id}: {result.get('error')}")
            except Exception as e:
                failed_count += 1
                errors.append(f"Error deleting {file_id}: {str(e)}")

        logger.info(f'Delete all files completed - Deleted: {deleted_count}/{total_count} - IP: {client_ip}')

        return jsonify({
            'success': True,
            'message': f'Deleted {deleted_count} files',
            'deleted_count': deleted_count,
            'failed_count': failed_count,
            'total_count': total_count,
            'errors': errors
        }), 200

    except Exception as e:
        logger.error(f'Delete all files exception - IP: {client_ip} - Error: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/documents/<path:document_name>', methods=['DELETE'])
def delete_document(document_name):
    """FileSearchStore 내부 문서 삭제 (REST API)"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'Document deletion request - Document: {document_name} - IP: {client_ip}')

        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        result = gemini.delete_document_from_store(document_name)

        if result['success']:
            logger.info(f'Document deletion successful - Document: {document_name} - IP: {client_ip}')
            return jsonify(result), 200
        else:
            logger.error(f'Document deletion failed - Document: {document_name} - Error: {result.get("error")} - IP: {client_ip}')
            return jsonify(result), 400

    except Exception as e:
        logger.error(f'Document deletion exception occurred - Document: {document_name} - IP: {client_ip} - Error: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/stores/<path:store_name>/documents', methods=['DELETE'])
def delete_all_documents(store_name):
    """FileSearchStore 내부 모든 문서 삭제"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'Delete all documents request - Store: {store_name} - IP: {client_ip}')

        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        result = gemini.delete_all_documents_from_store(store_name)

        if result['success']:
            logger.info(f'Delete all documents successful - Store: {store_name} - Deleted: {result["deleted_count"]}/{result["total_count"]} - IP: {client_ip}')
            return jsonify(result), 200
        else:
            logger.error(f'Delete all documents failed - Store: {store_name} - Error: {result.get("error")} - IP: {client_ip}')
            return jsonify(result), 400

    except Exception as e:
        logger.error(f'Delete all documents exception occurred - Store: {store_name} - IP: {client_ip} - Error: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/stores/<path:store_name>/documents/delete-by-category', methods=['POST'])
def delete_documents_by_category(store_name):
    """카테고리별로 문서 삭제"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        data = request.get_json()
        category = data.get('category', '').strip()

        if not category:
            logger.warning(f'Category is missing - Store: {store_name} - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'Category is required'}), 400

        logger.info(f'Delete documents by category request - Store: {store_name} - Category: {category} - IP: {client_ip}')

        # 해당 카테고리의 문서들 조회
        from app.db import get_all_mappings
        conn = sqlite3.connect('data/document_mappings.db')
        cursor = conn.cursor()
        cursor.execute('''
            SELECT document_name FROM document_mappings
            WHERE store_name = ? AND category = ?
        ''', (store_name, category))
        documents = cursor.fetchall()
        conn.close()

        if not documents:
            logger.info(f'No documents found for category - Store: {store_name} - Category: {category} - IP: {client_ip}')
            return jsonify({
                'success': True,
                'message': f'No documents found in category: {category}',
                'deleted_count': 0,
                'total_count': 0
            }), 200

        # 문서 삭제
        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        deleted_count = 0
        failed_count = 0
        errors = []

        for (doc_name,) in documents:
            try:
                result = gemini.delete_document_from_store(doc_name)
                if result['success']:
                    deleted_count += 1
                else:
                    failed_count += 1
                    errors.append(f"Failed to delete {doc_name}: {result.get('error')}")
            except Exception as e:
                failed_count += 1
                errors.append(f"Error deleting {doc_name}: {str(e)}")

        logger.info(f'Delete by category completed - Store: {store_name} - Category: {category} - Deleted: {deleted_count}/{len(documents)} - IP: {client_ip}')

        return jsonify({
            'success': True,
            'message': f'Deleted {deleted_count} documents from category: {category}',
            'deleted_count': deleted_count,
            'failed_count': failed_count,
            'total_count': len(documents),
            'errors': errors
        }), 200

    except Exception as e:
        logger.error(f'Delete by category exception - Store: {store_name} - IP: {client_ip} - Error: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== Search ====================

@bp.route('/api/search', methods=['POST'])
def search():
    """FileSearch로 검색 (활성 스토어 사용)"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'Search request - IP: {client_ip}')

        data = request.get_json()
        query = data.get('query', '').strip()
        metadata_filter = data.get('metadata_filter', None)
        history = data.get('history', [])

        if not query:
            logger.warning(f'Search query is missing - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'Query is required'}), 400

        # Get active stores from config (supports multiple stores)
        active_stores_json = get_config('active_stores')
        if active_stores_json:
            try:
                store_ids = json.loads(active_stores_json)
            except json.JSONDecodeError:
                store_ids = []
        else:
            # Fallback to single active store for backward compatibility
            active_store = get_config('active_store_name')
            store_ids = [active_store] if active_store else []

        if not store_ids:
            logger.warning(f'No active stores configured - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'No active FileStores configured. Please contact administrator.'}), 400

        logger.debug(f'Search started - Query: {query} - Active Stores: {store_ids} - History: {len(history)} messages - IP: {client_ip}')

        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        result = gemini.search_with_file_search(query, store_ids, metadata_filter, history=history)

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
        category = request.form.get('category', '').strip() or None

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

        converted_path = None
        try:
            # CSV 파일을 JSON으로 변환 (직접 업로드 시에도 변환 적용)
            converted_path, converted_filename = convert_csv_to_json(tmp_file_path, file.filename)
            final_file_path = converted_path
            final_filename = converted_filename

            logger.debug(f'FileStore upload attempt - File: {final_filename} - Store: {store_name} - Category: {category} - IP: {client_ip}')

            gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
            result = gemini.upload_and_import_to_store(
                file_path=final_file_path,
                store_name=store_name,
                display_name=final_filename,
                category=category
            )

            if result['success']:
                logger.info(f'FileStore upload successful - Original: {file.filename} - Final: {final_filename} - Store: {store_name} - Category: {category} - IP: {client_ip}')
                return jsonify(result), 201
            else:
                error_msg = result.get("error", "Unknown error")
                logger.error(f'FileStore upload failed - Original: {file.filename} - Final: {final_filename} - Error: {error_msg} - IP: {client_ip}')
                return jsonify({
                    'success': False,
                    'error': error_msg,
                    'original_file': file.filename,
                    'converted_file': final_filename
                }), 400

        finally:
            # 임시 파일 삭제
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)
            # 변환된 파일도 삭제 (원본과 다른 경우)
            if converted_path and converted_path != tmp_file_path and os.path.exists(converted_path):
                os.remove(converted_path)

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
        original_filename = data.get('original_filename', '').strip()
        category = data.get('category', '').strip() or None

        if not file_id or not store_name:
            logger.warning(f'File ID or store name is missing - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'File ID and store name are required'}), 400

        logger.debug(f'File import attempt - File: {file_id} - Store: {store_name} - Filename: {original_filename} - Category: {category} - IP: {client_ip}')

        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        result = gemini.import_file_to_store(
            file_id=file_id,
            store_name=store_name,
            original_filename=original_filename,
            category=category
        )

        if result['success']:
            logger.info(f'File import successful - File: {file_id} - Store: {store_name} - Category: {category} - IP: {client_ip}')
            return jsonify(result), 201
        else:
            logger.error(f'File import failed - File: {file_id} - Error: {result.get("error")} - IP: {client_ip}')
            return jsonify(result), 400

    except Exception as e:
        logger.error(f'File import exception occurred - IP: {client_ip} - Error: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== Config Management ====================

@bp.route('/api/config/active-store', methods=['GET'])
def get_active_store():
    """활성 FileStore 조회"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'Get active store request - IP: {client_ip}')

        active_store = get_config('active_store_name')

        logger.info(f'Active store retrieved: {active_store} - IP: {client_ip}')
        return jsonify({
            'success': True,
            'active_store_name': active_store
        }), 200

    except Exception as e:
        logger.error(f'Get active store exception - IP: {client_ip} - Error: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/config/active-store', methods=['POST'])
def set_active_store():
    """활성 FileStore 설정"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'Set active store request - IP: {client_ip}')

        data = request.get_json()
        store_name = data.get('store_name', '').strip()

        if not store_name:
            logger.warning(f'Store name is missing - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'Store name is required'}), 400

        # Store name 유효성 검증 (실제 존재하는지)
        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        store_info = gemini.get_file_search_store(store_name)

        if not store_info.get('success'):
            logger.warning(f'Invalid store name - Store: {store_name} - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'Invalid FileStore name'}), 400

        # Config에 저장
        if set_config('active_store_name', store_name):
            logger.info(f'Active store set successfully - Store: {store_name} - IP: {client_ip}')
            return jsonify({
                'success': True,
                'active_store_name': store_name,
                'message': 'Active FileStore set successfully'
            }), 200
        else:
            logger.error(f'Failed to set active store - Store: {store_name} - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'Failed to save configuration'}), 500

    except Exception as e:
        logger.error(f'Set active store exception - IP: {client_ip} - Error: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/config/active-stores', methods=['GET'])
def get_active_stores():
    """활성 FileStore 목록 조회 (다중 선택)"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'Get active stores request - IP: {client_ip}')

        # JSON으로 저장된 다중 active stores 조회
        active_stores_json = get_config('active_stores')
        if active_stores_json:
            try:
                active_stores = json.loads(active_stores_json)
            except json.JSONDecodeError:
                # JSON 파싱 실패 시 빈 리스트
                active_stores = []
        else:
            # 새 설정이 없으면 기존 단일 active_store_name을 사용
            active_store = get_config('active_store_name')
            active_stores = [active_store] if active_store else []

        logger.info(f'Active stores retrieved: {active_stores} - IP: {client_ip}')
        return jsonify({
            'success': True,
            'active_stores': active_stores
        }), 200

    except Exception as e:
        logger.error(f'Get active stores exception - IP: {client_ip} - Error: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/config/active-stores', methods=['POST'])
def set_active_stores():
    """활성 FileStore 목록 설정 (다중 선택)"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'Set active stores request - IP: {client_ip}')

        data = request.get_json()
        store_names = data.get('store_names', [])

        if not store_names or not isinstance(store_names, list):
            logger.warning(f'Store names missing or invalid - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'Store names array is required'}), 400

        if len(store_names) == 0:
            logger.warning(f'Empty store names list - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'At least one store must be selected'}), 400

        # Store names 유효성 검증
        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        invalid_stores = []
        for store_name in store_names:
            store_info = gemini.get_file_search_store(store_name)
            if not store_info.get('success'):
                invalid_stores.append(store_name)

        if invalid_stores:
            logger.warning(f'Invalid store names: {invalid_stores} - IP: {client_ip}')
            return jsonify({'success': False, 'error': f'Invalid FileStore names: {", ".join(invalid_stores)}'}), 400

        # Config에 JSON으로 저장
        active_stores_json = json.dumps(store_names)
        if set_config('active_stores', active_stores_json):
            logger.info(f'Active stores set successfully - Stores: {store_names} - IP: {client_ip}')
            return jsonify({
                'success': True,
                'active_stores': store_names,
                'message': f'Active FileStores set successfully ({len(store_names)} stores)'
            }), 200
        else:
            logger.error(f'Failed to set active stores - Stores: {store_names} - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'Failed to save configuration'}), 500

    except Exception as e:
        logger.error(f'Set active stores exception - IP: {client_ip} - Error: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== Wayfinding (길찾기) Routes ====================

@bp.route('/api/wayfinding/facilities', methods=['GET'])
def get_facilities():
    """시설물 목록 조회"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'Facilities list request - IP: {client_ip}')

        service = get_wayfinding_service()
        facility_names = service.get_facility_names()

        logger.info(f'Facilities list retrieval successful - Count: {len(facility_names)} - IP: {client_ip}')
        return jsonify({
            'success': True,
            'facilities': facility_names,
            'count': len(facility_names)
        }), 200

    except Exception as e:
        logger.error(f'Facilities list retrieval exception - IP: {client_ip} - Error: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/wayfinding/find-path', methods=['POST'])
def find_path():
    """최단 경로 찾기"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'Path finding request - IP: {client_ip}')

        data = request.get_json()
        start_name = data.get('start', '').strip()
        end_name = data.get('end', '').strip()

        if not start_name or not end_name:
            logger.warning(f'Start or end location is missing - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'Start and end locations are required'}), 400

        if start_name == end_name:
            logger.warning(f'Start and end are the same - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'Start and end locations must be different'}), 400

        logger.debug(f'Finding path - Start: {start_name} - End: {end_name} - IP: {client_ip}')

        service = get_wayfinding_service()
        result = service.find_path(start_name, end_name)

        if result['success']:
            logger.info(f'Path found successfully - Start: {start_name} - End: {end_name} - Distance: {result.get("distance")} - IP: {client_ip}')
            return jsonify(result), 200
        else:
            logger.warning(f'Path finding failed - Start: {start_name} - End: {end_name} - Error: {result.get("message")} - IP: {client_ip}')
            return jsonify(result), 400

    except Exception as e:
        logger.error(f'Path finding exception - IP: {client_ip} - Error: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/wayfinding/find-path-coords', methods=['POST'])
def find_path_coords():
    """좌표 기반 최단 경로 찾기 (지도 클릭)"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'Coordinate-based path finding request - IP: {client_ip}')

        data = request.get_json()
        start_x = data.get('start_x')
        start_y = data.get('start_y')
        end_x = data.get('end_x')
        end_y = data.get('end_y')

        if None in [start_x, start_y, end_x, end_y]:
            logger.warning(f'Missing coordinates - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'All coordinates (start_x, start_y, end_x, end_y) are required'}), 400

        logger.debug(f'Finding path - Start: ({start_x}, {start_y}) - End: ({end_x}, {end_y}) - IP: {client_ip}')

        service = get_wayfinding_service()
        result = service.find_path_from_coords(start_x, start_y, end_x, end_y)

        if result['success']:
            logger.info(f'Path found successfully - Distance: {result.get("distance")} - IP: {client_ip}')
            return jsonify(result), 200
        else:
            logger.warning(f'Path finding failed - Error: {result.get("message")} - IP: {client_ip}')
            return jsonify(result), 400

    except Exception as e:
        logger.error(f'Coordinate-based path finding exception - IP: {client_ip} - Error: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/wayfinding/nearest-facility', methods=['POST'])
def find_nearest_facility():
    """가장 가까운 특정 시설물 찾기"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'Nearest facility request - IP: {client_ip}')

        data = request.get_json()
        x = data.get('x')
        y = data.get('y')
        category = data.get('category', 'toilet')
        name_pattern = data.get('name_pattern')

        if x is None or y is None:
            logger.warning(f'Missing coordinates - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'Coordinates (x, y) are required'}), 400

        search_term = name_pattern if name_pattern else category
        logger.debug(f'Finding nearest {search_term} - Location: ({x}, {y}) - IP: {client_ip}')

        service = get_wayfinding_service()
        result = service.find_nearest_facility_by_category(x, y, category, name_pattern)

        if result['success']:
            logger.info(f'Nearest facility found - Category: {category} - IP: {client_ip}')
            return jsonify(result), 200
        else:
            logger.warning(f'Nearest facility search failed - Error: {result.get("message")} - IP: {client_ip}')
            return jsonify(result), 400

    except Exception as e:
        logger.error(f'Nearest facility exception - IP: {client_ip} - Error: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500
