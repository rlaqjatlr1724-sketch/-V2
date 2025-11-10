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
    logger.info(f'인덱스 페이지 요청 - IP: {request.remote_addr}')
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f'인덱스 페이지 렌더링 실패 - IP: {request.remote_addr} - 에러: {str(e)}')
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== FileSearchStore Management ====================

@bp.route('/api/stores/create', methods=['POST'])
def create_store():
    """새 FileSearchStore 생성"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'스토어 생성 요청 - IP: {client_ip}')

        data = request.get_json()
        store_name = data.get('name', '').strip()

        if not store_name:
            logger.warning(f'스토어 이름 누락 - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'Store name is required'}), 400

        logger.debug(f'스토어 생성 시도 - 이름: {store_name} - IP: {client_ip}')

        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        result = gemini.create_file_search_store(store_name)

        if result['success']:
            logger.info(f'스토어 생성 성공 - 이름: {store_name} - 스토어ID: {result.get("store_name")} - IP: {client_ip}')
            return jsonify(result), 201
        else:
            logger.error(f'스토어 생성 실패 - 이름: {store_name} - 에러: {result.get("error")} - IP: {client_ip}')
            return jsonify(result), 400

    except Exception as e:
        logger.error(f'스토어 생성 예외 발생 - IP: {client_ip} - 에러: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/stores', methods=['GET'])
def list_stores():
    """모든 FileSearchStore 조회"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'스토어 목록 조회 요청 - IP: {client_ip}')

        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        result = gemini.list_file_search_stores()

        if result['success']:
            store_count = result.get('count', 0)
            logger.info(f'스토어 목록 조회 성공 - 개수: {store_count} - IP: {client_ip}')
            logger.debug(f'조회된 스토어: {result.get("stores")} - IP: {client_ip}')
            return jsonify(result), 200
        else:
            logger.error(f'스토어 목록 조회 실패 - 에러: {result.get("error")} - IP: {client_ip}')
            return jsonify(result), 400

    except Exception as e:
        logger.error(f'스토어 목록 조회 예외 발생 - IP: {client_ip} - 에러: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/stores/<path:store_id>', methods=['GET'])
def get_store(store_id):
    """특정 FileSearchStore 조회"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'스토어 조회 요청 - 스토어ID: {store_id} - IP: {client_ip}')

        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        result = gemini.get_file_search_store(store_id)

        if result['success']:
            logger.info(f'스토어 조회 성공 - 스토어ID: {store_id} - IP: {client_ip}')
            logger.debug(f'스토어 정보: {result} - IP: {client_ip}')
            return jsonify(result), 200
        else:
            logger.warning(f'스토어 조회 실패 - 스토어ID: {store_id} - 에러: {result.get("error")} - IP: {client_ip}')
            return jsonify(result), 404

    except Exception as e:
        logger.error(f'스토어 조회 예외 발생 - 스토어ID: {store_id} - IP: {client_ip} - 에러: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/stores/<path:store_id>', methods=['DELETE'])
def delete_store(store_id):
    """FileSearchStore 삭제"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'스토어 삭제 요청 - 스토어ID: {store_id} - IP: {client_ip}')

        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        result = gemini.delete_file_search_store(store_id)

        if result['success']:
            logger.info(f'스토어 삭제 성공 - 스토어ID: {store_id} - IP: {client_ip}')
            return jsonify(result), 200
        else:
            logger.error(f'스토어 삭제 실패 - 스토어ID: {store_id} - 에러: {result.get("error")} - IP: {client_ip}')
            return jsonify(result), 400

    except Exception as e:
        logger.error(f'스토어 삭제 예외 발생 - 스토어ID: {store_id} - IP: {client_ip} - 에러: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== File Management ====================

@bp.route('/api/files/upload', methods=['POST'])
def upload_file():
    """파일 업로드 (Files API)"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'파일 업로드 요청 - IP: {client_ip}')

        if 'file' not in request.files:
            logger.warning(f'파일 누락 - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'No file provided'}), 400

        file = request.files['file']
        if file.filename == '':
            logger.warning(f'파일명 없음 - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            logger.warning(f'허용되지 않은 파일 형식 - 파일명: {file.filename} - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'File type not allowed'}), 400

        logger.debug(f'파일 업로드 시작 - 파일명: {file.filename} - IP: {client_ip}')

        # 임시 파일에 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            file.save(tmp.name)
            tmp_path = tmp.name

        try:
            # Gemini Files API를 통해 파일 업로드
            gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
            result = gemini.upload_file(tmp_path)

            if result['success']:
                logger.info(f'파일 업로드 성공 - 파일명: {file.filename} - 파일ID: {result.get("file_id")} - IP: {client_ip}')
                logger.debug(f'업로드 결과: {result} - IP: {client_ip}')
                return jsonify(result), 201
            else:
                logger.error(f'파일 업로드 실패 - 파일명: {file.filename} - 에러: {result.get("error")} - IP: {client_ip}')
                return jsonify(result), 400
        finally:
            # 임시 파일 삭제
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
                logger.debug(f'임시 파일 삭제 완료 - 경로: {tmp_path} - IP: {client_ip}')

    except Exception as e:
        logger.error(f'파일 업로드 예외 발생 - IP: {client_ip} - 에러: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/files/<path:file_id>/import', methods=['POST'])
def import_file(file_id):
    """파일을 FileSearchStore로 임포트"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'파일 임포트 요청 - 파일ID: {file_id} - IP: {client_ip}')

        data = request.get_json()
        store_id = data.get('store_id', '').strip()
        metadata = data.get('metadata', None)

        if not store_id:
            logger.warning(f'스토어ID 누락 - 파일ID: {file_id} - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'store_id is required'}), 400

        logger.debug(f'파일 임포트 시도 - 파일ID: {file_id} - 스토어ID: {store_id} - 메타데이터: {metadata} - IP: {client_ip}')

        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        result = gemini.import_file_to_store(file_id, store_id, metadata)

        if result['success']:
            logger.info(f'파일 임포트 성공 - 파일ID: {file_id} - 스토어ID: {store_id} - IP: {client_ip}')
            return jsonify(result), 200
        else:
            logger.error(f'파일 임포트 실패 - 파일ID: {file_id} - 스토어ID: {store_id} - 에러: {result.get("error")} - IP: {client_ip}')
            return jsonify(result), 400

    except Exception as e:
        logger.error(f'파일 임포트 예외 발생 - 파일ID: {file_id} - IP: {client_ip} - 에러: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/files', methods=['GET'])
def list_files():
    """모든 파일 조회"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'파일 목록 조회 요청 - IP: {client_ip}')

        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        result = gemini.list_files()

        if result['success']:
            file_count = result.get('count', 0)
            logger.info(f'파일 목록 조회 성공 - 개수: {file_count} - IP: {client_ip}')
            logger.debug(f'조회된 파일: {result.get("files")} - IP: {client_ip}')
            return jsonify(result), 200
        else:
            logger.error(f'파일 목록 조회 실패 - 에러: {result.get("error")} - IP: {client_ip}')
            return jsonify(result), 400

    except Exception as e:
        logger.error(f'파일 목록 조회 예외 발생 - IP: {client_ip} - 에러: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/files/<path:file_id>', methods=['GET'])
def get_file_info(file_id):
    """특정 파일 정보 조회"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'파일 정보 조회 요청 - 파일ID: {file_id} - IP: {client_ip}')

        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        result = gemini.get_file(file_id)

        if result['success']:
            logger.info(f'파일 정보 조회 성공 - 파일ID: {file_id} - IP: {client_ip}')
            logger.debug(f'파일 정보: {result} - IP: {client_ip}')
            return jsonify(result), 200
        else:
            logger.warning(f'파일 정보 조회 실패 - 파일ID: {file_id} - 에러: {result.get("error")} - IP: {client_ip}')
            return jsonify(result), 404

    except Exception as e:
        logger.error(f'파일 정보 조회 예외 발생 - 파일ID: {file_id} - IP: {client_ip} - 에러: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

@bp.route('/api/files/<path:file_id>', methods=['DELETE'])
def delete_file(file_id):
    """파일 삭제"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'파일 삭제 요청 - 파일ID: {file_id} - IP: {client_ip}')

        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        result = gemini.delete_file(file_id)

        if result['success']:
            logger.info(f'파일 삭제 성공 - 파일ID: {file_id} - IP: {client_ip}')
            return jsonify(result), 200
        else:
            logger.error(f'파일 삭제 실패 - 파일ID: {file_id} - 에러: {result.get("error")} - IP: {client_ip}')
            return jsonify(result), 400

    except Exception as e:
        logger.error(f'파일 삭제 예외 발생 - 파일ID: {file_id} - IP: {client_ip} - 에러: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== Search ====================

@bp.route('/api/search', methods=['POST'])
def search():
    """FileSearch로 검색"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'검색 요청 - IP: {client_ip}')

        data = request.get_json()
        query = data.get('query', '').strip()
        store_ids = data.get('store_ids', [])
        metadata_filter = data.get('metadata_filter', None)

        if not query:
            logger.warning(f'검색 쿼리 누락 - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'Query is required'}), 400

        if not store_ids:
            logger.warning(f'스토어ID 누락 - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'store_ids is required'}), 400

        if not isinstance(store_ids, list):
            logger.warning(f'잘못된 store_ids 형식 - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'store_ids must be an array'}), 400

        logger.debug(f'검색 시작 - 쿼리: {query} - 스토어: {store_ids} - 메타데이터 필터: {metadata_filter} - IP: {client_ip}')

        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        result = gemini.search_with_file_search(query, store_ids, metadata_filter)

        if result['success']:
            logger.info(f'검색 성공 - 쿼리: {query} - 스토어: {store_ids} - IP: {client_ip}')
            logger.debug(f'검색 결과 길이: {len(result.get("result", ""))} 문자 - IP: {client_ip}')
            return jsonify(result), 200
        else:
            logger.error(f'검색 실패 - 쿼리: {query} - 에러: {result.get("error")} - IP: {client_ip}')
            return jsonify(result), 400

    except Exception as e:
        logger.error(f'검색 예외 발생 - IP: {client_ip} - 에러: {str(e)}', exc_info=True)
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
    
    logger.info(f'파일 미리보기 요청 - File ID: {file_id}, IP: {client_ip}')
    try:
        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        file_info = gemini.get_file(file_id)
        
        if not file_info.get('success'):
            logger.warning(f'파일 조회 실패 - File ID: {file_id}')
            return jsonify({'success': False, 'error': 'File not found'}), 404
        
        # 파일 URI를 반환 (클라이언트에서 직접 접근 가능)
        file_uri = file_info.get('uri')
        if not file_uri:
            logger.warning(f'파일 URI 없음 - File ID: {file_id}')
            return jsonify({'success': False, 'error': 'File URI not available'}), 400
        
        logger.info(f'파일 미리보기 정보 반환 - File ID: {file_id}')
        return jsonify({
            'success': True,
            'file_id': file_id,
            'display_name': file_info.get('display_name'),
            'mime_type': file_info.get('mime_type'),
            'size_bytes': file_info.get('size_bytes'),
            'uri': file_uri
        }), 200
    except Exception as e:
        logger.error(f'파일 미리보기 중 오류 발생: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== FileStore Direct Upload ====================

@bp.route('/api/stores/upload', methods=['POST'])
def upload_to_store():
    """FileStore에 파일 직접 업로드 (uploadToFileSearchStore)"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'FileStore 직접 업로드 요청 - IP: {client_ip}')

        # 요청 데이터 검증
        if 'file' not in request.files:
            logger.warning(f'파일 없음 - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'No file provided'}), 400

        file = request.files['file']
        store_name = request.form.get('store_name', '').strip()

        if not file or not store_name:
            logger.warning(f'파일 또는 스토어 이름 누락 - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'File and store name are required'}), 400

        if not allowed_file(file.filename):
            logger.warning(f'지원하지 않는 파일 형식 - 파일명: {file.filename} - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'File type not allowed'}), 400

        # 임시 파일에 저장
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp_file:
            file.save(tmp_file.name)
            tmp_file_path = tmp_file.name

        try:
            logger.debug(f'FileStore 업로드 시도 - 파일: {file.filename} - 스토어: {store_name} - IP: {client_ip}')

            gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
            result = gemini.upload_and_import_to_store(
                file_path=tmp_file_path,
                store_name=store_name,
                display_name=file.filename
            )

            if result['success']:
                logger.info(f'FileStore 업로드 성공 - 파일: {file.filename} - 스토어: {store_name} - IP: {client_ip}')
                return jsonify(result), 201
            else:
                logger.error(f'FileStore 업로드 실패 - 파일: {file.filename} - 에러: {result.get("error")} - IP: {client_ip}')
                return jsonify(result), 400

        finally:
            # 임시 파일 삭제
            if os.path.exists(tmp_file_path):
                os.remove(tmp_file_path)

    except Exception as e:
        logger.error(f'FileStore 업로드 중 예외 발생 - IP: {client_ip} - 에러: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500

# ==================== File Import to Store ====================

@bp.route('/api/files/import', methods=['POST'])
def import_file_to_store():
    """Files API의 파일을 FileStore로 import"""
    logger = get_logger()
    client_ip = request.remote_addr

    try:
        logger.info(f'파일 import 요청 - IP: {client_ip}')

        data = request.get_json()
        file_id = data.get('file_id', '').strip()
        store_name = data.get('store_name', '').strip()

        if not file_id or not store_name:
            logger.warning(f'파일 ID 또는 스토어 이름 누락 - IP: {client_ip}')
            return jsonify({'success': False, 'error': 'File ID and store name are required'}), 400

        logger.debug(f'파일 import 시도 - 파일: {file_id} - 스토어: {store_name} - IP: {client_ip}')

        gemini = GeminiClient(current_app.config['GEMINI_API_KEY'])
        result = gemini.import_file_to_store(
            file_id=file_id,
            store_name=store_name
        )

        if result['success']:
            logger.info(f'파일 import 성공 - 파일: {file_id} - 스토어: {store_name} - IP: {client_ip}')
            return jsonify(result), 201
        else:
            logger.error(f'파일 import 실패 - 파일: {file_id} - 에러: {result.get("error")} - IP: {client_ip}')
            return jsonify(result), 400

    except Exception as e:
        logger.error(f'파일 import 중 예외 발생 - IP: {client_ip} - 에러: {str(e)}', exc_info=True)
        return jsonify({'success': False, 'error': str(e)}), 500
