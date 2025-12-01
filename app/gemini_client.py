"""
Gemini Client using the new google.genai SDK
Implements FileSearchStore API for document search and retrieval
"""
from google import genai
from google.genai import types
from typing import Optional, List, Dict, Any
import os
from pathlib import Path
from app.logger import get_logger
from app.db import save_mapping, get_mapping, delete_mapping


class GeminiClient:
    """Client for interacting with Gemini API using google.genai SDK"""

    def __init__(self, api_key: str):
        """
        Initialize Gemini client with API key

        Args:
            api_key: Google AI API key for authentication
        """
        self.api_key = api_key
        self.logger = get_logger()

        # Configure the client with API key
        self.client = genai.Client(api_key=api_key)        
        self.logger.info("GeminiClient initialized successfully")


    # ==================== FileSearchStore Methods ====================

    def create_file_search_store(self, display_name: str) -> Dict[str, Any]:
        """
        Create a new FileSearchStore

        Args:
            display_name: Display name for the store

        Returns:
            Dict with success status and store information
        """
        try:
            self.logger.info(f"Creating FileSearchStore with display_name: {display_name}")

            store = self.client.file_search_stores.create(
                config={'display_name': display_name}
            )

            self.logger.info(f"FileSearchStore created successfully: {store.name}")
            return {
                "success": True,
                "store_name": store.name,
                "display_name": store.display_name,
                "create_time": str(store.create_time) if hasattr(store, 'create_time') else None,
                "update_time": str(store.update_time) if hasattr(store, 'update_time') else None
            }
        except Exception as e:
            self.logger.error(f"Error creating FileSearchStore: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }

    def list_file_search_stores(self) -> Dict[str, Any]:
        """
        List all FileSearchStores

        Returns:
            Dict with success status and list of stores
        """
        try:
            self.logger.info("Listing all FileSearchStores")

            stores = self.client.file_search_stores.list()
            store_list = []

            for store in stores:
                store_info = {
                    "store_name": store.name,
                    "display_name": store.display_name,
                    "create_time": str(store.create_time) if hasattr(store, 'create_time') else None,
                    "update_time": str(store.update_time) if hasattr(store, 'update_time') else None,
                    "active_documents_count": int(store.active_documents_count) if (hasattr(store, 'active_documents_count') and store.active_documents_count is not None) else 0,
                    "pending_documents_count": int(store.pending_documents_count) if (hasattr(store, 'pending_documents_count') and store.pending_documents_count is not None) else 0,
                    "failed_documents_count": int(store.failed_documents_count) if (hasattr(store, 'failed_documents_count') and store.failed_documents_count is not None) else 0,
                    "size_bytes": int(store.size_bytes) if (hasattr(store, 'size_bytes') and store.size_bytes is not None) else 0
                }
                store_list.append(store_info)

            self.logger.info(f"Found {len(store_list)} FileSearchStores")
            return {
                "success": True,
                "stores": store_list,
                "count": len(store_list)
            }
        except Exception as e:
            self.logger.error(f"Error listing FileSearchStores: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "stores": []
            }

    def get_file_search_store(self, store_name: str) -> Dict[str, Any]:
        """
        Get a specific FileSearchStore by name

        Args:
            store_name: Name of the store to retrieve

        Returns:
            Dict with success status and store information
        """
        try:
            self.logger.info(f"Getting FileSearchStore: {store_name}")

            store = self.client.file_search_stores.get(name=store_name)

            self.logger.info(f"FileSearchStore retrieved successfully: {store_name}")
            return {
                "success": True,
                "store_name": store.name,
                "display_name": store.display_name,
                "create_time": str(store.create_time) if hasattr(store, 'create_time') else None,
                "update_time": str(store.update_time) if hasattr(store, 'update_time') else None,
                "active_documents_count": int(store.active_documents_count) if (hasattr(store, 'active_documents_count') and store.active_documents_count is not None) else 0,
                "pending_documents_count": int(store.pending_documents_count) if (hasattr(store, 'pending_documents_count') and store.pending_documents_count is not None) else 0,
                "failed_documents_count": int(store.failed_documents_count) if (hasattr(store, 'failed_documents_count') and store.failed_documents_count is not None) else 0,
                "size_bytes": int(store.size_bytes) if (hasattr(store, 'size_bytes') and store.size_bytes is not None) else 0
            }
        except Exception as e:
            self.logger.error(f"Error getting FileSearchStore {store_name}: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }

    def delete_file_search_store(self, store_name: str) -> Dict[str, Any]:
        """
        Delete a FileSearchStore

        Args:
            store_name: Name of the store to delete

        Returns:
            Dict with success status
        """
        try:
            self.logger.info(f"Deleting FileSearchStore: {store_name}")

            self.client.file_search_stores.delete(name=store_name)

            self.logger.info(f"FileSearchStore deleted successfully: {store_name}")
            return {
                "success": True,
                "message": f"FileSearchStore {store_name} deleted successfully"
            }
        except Exception as e:
            self.logger.error(f"Error deleting FileSearchStore {store_name}: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }

    def list_documents_in_store(self, store_name: str, page_size: int = 20) -> Dict[str, Any]:
        """
        List all documents in a FileSearchStore

        Args:
            store_name: Name of the FileSearchStore (format: fileSearchStores/{id})
            page_size: Maximum documents per page (default: 20)

        Returns:
            Dict with success status and list of documents
        """
        try:
            self.logger.info(f"Listing documents in FileSearchStore: {store_name}")

            # Use SDK to list documents (without page_size parameter)
            documents = self.client.file_search_stores.documents.list(
                parent=store_name
            )

            document_list = []
            for idx, doc in enumerate(documents):
                # Try to get original filename from mapping
                original_filename = get_mapping(doc.name)
                display_name = original_filename if original_filename else (doc.display_name if hasattr(doc, 'display_name') else None)

                doc_info = {
                    "document_name": doc.name,
                    "display_name": display_name,
                    "mime_type": doc.mime_type if hasattr(doc, 'mime_type') else None,
                    "create_time": doc.create_time if hasattr(doc, 'create_time') else None,
                    "update_time": doc.update_time if hasattr(doc, 'update_time') else None,
                    "size_bytes": doc.size_bytes if hasattr(doc, 'size_bytes') else None,
                }
                document_list.append(doc_info)

            self.logger.info(f"Found {len(document_list)} documents in store {store_name}")
            return {
                "success": True,
                "documents": document_list,
                "count": len(document_list),
                "store_name": store_name
            }
        except Exception as e:
            self.logger.error(f"Error listing documents in store {store_name}: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "documents": []
            }

    def delete_document_from_store(self, document_name: str, force: bool = True) -> Dict[str, Any]:
        """
        Delete a document from a FileSearchStore

        Args:
            document_name: Full name of the document to delete (e.g., 'fileSearchStores/xxx/documents/yyy')
            force: If True, also delete associated chunks (default: True)

        Returns:
            Dict with success status
        """
        try:
            self.logger.info(f"Deleting document from FileSearchStore: {document_name}")

            # Use SDK to delete document
            self.client.file_search_stores.documents.delete(
                name=document_name,
                config={'force': force}
            )

            # Delete mapping from database
            delete_mapping(document_name)

            self.logger.info(f"Document deleted successfully: {document_name}")
            return {
                "success": True,
                "message": f"Document {document_name} deleted successfully"
            }
        except Exception as e:
            self.logger.error(f"Error deleting document {document_name}: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }

    def delete_all_documents_from_store(self, store_name: str, force: bool = True) -> Dict[str, Any]:
        """
        Delete all documents from a FileSearchStore

        Args:
            store_name: Name of the FileSearchStore (format: fileSearchStores/{id})
            force: If True, also delete associated chunks (default: True)

        Returns:
            Dict with success status, deleted count, and any errors
        """
        try:
            self.logger.info(f"Deleting all documents from FileSearchStore: {store_name}")

            # First, get all documents
            documents_result = self.list_documents_in_store(store_name)
            if not documents_result['success']:
                return {
                    "success": False,
                    "error": "Failed to list documents",
                    "deleted_count": 0
                }

            documents = documents_result['documents']
            total_count = len(documents)
            deleted_count = 0
            failed_count = 0
            errors = []

            self.logger.info(f"Found {total_count} documents to delete")

            # Delete each document
            for doc in documents:
                doc_name = doc['document_name']
                try:
                    self.client.file_search_stores.documents.delete(
                        name=doc_name,
                        config={'force': force}
                    )
                    # Delete mapping from database
                    delete_mapping(doc_name)
                    deleted_count += 1
                    self.logger.debug(f"Deleted document: {doc_name}")
                except Exception as e:
                    failed_count += 1
                    error_msg = f"Failed to delete {doc_name}: {str(e)}"
                    errors.append(error_msg)
                    self.logger.error(error_msg)

            self.logger.info(f"Deletion complete: {deleted_count} deleted, {failed_count} failed")

            return {
                "success": True,
                "message": f"Deleted {deleted_count} out of {total_count} documents",
                "deleted_count": deleted_count,
                "failed_count": failed_count,
                "total_count": total_count,
                "errors": errors
            }
        except Exception as e:
            self.logger.error(f"Error deleting all documents from store {store_name}: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "deleted_count": 0
            }

    # ==================== File Management Methods ====================

    def upload_file(self, file_path: str, display_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload a file to Files API

        Args:
            file_path: Path to the file to upload
            display_name: Optional display name for the file (original filename)

        Returns:
            Dict with success status and file information
        """
        try:
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                self.logger.error(f"File not found: {file_path}")
                return {
                    "success": False,
                    "error": f"File not found: {file_path}"
                }

            # Use provided display_name or fallback to file basename
            final_display_name = display_name or os.path.basename(file_path)
            self.logger.info(f"Uploading file: {file_path} with display_name: {final_display_name}")

            # Upload file using Files API - pass file path as string
            uploaded_file = self.client.files.upload(
                file=file_path,
                config={'display_name': final_display_name}
            )

            self.logger.info(f"File uploaded successfully: {uploaded_file.name}")
            return {
                "success": True,
                "file_id": uploaded_file.name,
                "display_name": uploaded_file.display_name,
                "mime_type": uploaded_file.mime_type if hasattr(uploaded_file, 'mime_type') else None,
                "size_bytes": uploaded_file.size_bytes if hasattr(uploaded_file, 'size_bytes') else None,
                "create_time": str(uploaded_file.create_time) if hasattr(uploaded_file, 'create_time') else None,
                "update_time": str(uploaded_file.update_time) if hasattr(uploaded_file, 'update_time') else None,
                "uri": uploaded_file.uri if hasattr(uploaded_file, 'uri') else None
            }
        except Exception as e:
            self.logger.error(f"Error uploading file {file_path}: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }

    def import_file_to_store(self, file_id: str, store_name: str, original_filename: Optional[str] = None) -> Dict[str, Any]:
        """
        Import a file from Files API to a FileSearchStore

        Args:
            file_id: ID of the file to import (from Files API)
            store_name: Name of the target FileSearchStore
            original_filename: Original filename to save in mapping

        Returns:
            Dict with success status
        """
        try:
            self.logger.info(f"Importing file {file_id} to store {store_name}")

            result = self.client.file_search_stores.import_file(
                file_search_store_name=store_name,
                file_name=file_id
            )

            self.logger.info(f"File imported successfully to store {store_name}: {result}")

            # Extract document_name from operation.name
            # operation.name format: fileSearchStores/{store_id}/operations/{file_id}-{random_id}
            # document_name format: fileSearchStores/{store_id}/documents/{file_id}-{random_id}
            if hasattr(result, 'name') and result.name and original_filename:
                document_name = result.name.replace('/operations/', '/documents/')
                save_mapping(document_name, original_filename, file_id, store_name)
                self.logger.info(f"Saved mapping: {document_name} -> {original_filename}")

            return {
                "success": True,
                "file_id": file_id,
                "store_name": store_name,
                "message": "File imported successfully"
            }
        except Exception as e:
            self.logger.error(f"Error importing file {file_id} to store {store_name}: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }

    def upload_and_import_to_store(self, file_path: str, store_name: str, display_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Upload a file and directly import it to a FileSearchStore

        Args:
            file_path: Path to the file to upload
            store_name: Name of the target FileSearchStore (format: fileSearchStores/{id})
            display_name: Optional display name for the file

        Returns:
            Dict with success status and file information
        """
        try:
            file_path_obj = Path(file_path)
            if not file_path_obj.exists():
                self.logger.error(f"File not found: {file_path}")
                return {
                    "success": False,
                    "error": f"File not found: {file_path}"
                }

            self.logger.info(f"Uploading and importing file {file_path} to store {store_name}")

            # Use SDK to upload file directly to FileSearchStore
            uploaded_file = self.client.file_search_stores.documents.upload_to_file_search_store(
                file=file_path,
                store_id=store_name,
                display_name=display_name or os.path.basename(file_path)
            )

            self.logger.info(f"File uploaded and imported successfully to store {store_name}")
            return {
                "success": True,
                "store_name": store_name,
                "file_path": file_path,
                "document_name": uploaded_file.name if hasattr(uploaded_file, 'name') else None,
                "message": "File uploaded and imported successfully"
            }
        except Exception as e:
            self.logger.error(f"Error uploading and importing file {file_path} to store {store_name}: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }

    def delete_file(self, file_id: str) -> Dict[str, Any]:
        """
        Delete a file from Files API

        Args:
            file_id: ID of the file to delete

        Returns:
            Dict with success status
        """
        try:
            self.logger.info(f"Deleting file: {file_id}")

            self.client.files.delete(name=file_id)

            self.logger.info(f"File deleted successfully: {file_id}")
            return {
                "success": True,
                "file_id": file_id,
                "message": f"File {file_id} deleted successfully"
            }
        except Exception as e:
            self.logger.error(f"Error deleting file {file_id}: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }

    def list_files(self) -> Dict[str, Any]:
        """
        List all uploaded files

        Returns:
            Dict with success status and list of files
        """
        try:
            self.logger.info("Listing all files")

            files = self.client.files.list()
            file_list = []

            for file in files:
                file_info = {
                    "file_id": file.name,
                    "display_name": file.display_name,
                    "mime_type": file.mime_type if hasattr(file, 'mime_type') else None,
                    "size_bytes": file.size_bytes if hasattr(file, 'size_bytes') else None,
                    "create_time": str(file.create_time) if hasattr(file, 'create_time') else None,
                    "update_time": str(file.update_time) if hasattr(file, 'update_time') else None,
                    "uri": file.uri if hasattr(file, 'uri') else None
                }
                file_list.append(file_info)

            self.logger.info(f"Found {len(file_list)} files")
            return {
                "success": True,
                "files": file_list,
                "count": len(file_list)
            }
        except Exception as e:
            self.logger.error(f"Error listing files: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "files": []
            }

    def get_file(self, file_id: str) -> Dict[str, Any]:
        """
        Get information about a specific file

        Args:
            file_id: ID of the file to retrieve

        Returns:
            Dict with success status and file information
        """
        try:
            self.logger.info(f"Getting file info: {file_id}")

            file = self.client.files.get(name=file_id)

            self.logger.info(f"File info retrieved successfully: {file_id}")
            return {
                "success": True,
                "file_id": file.name,
                "display_name": file.display_name,
                "mime_type": file.mime_type if hasattr(file, 'mime_type') else None,
                "size_bytes": file.size_bytes if hasattr(file, 'size_bytes') else None,
                "create_time": str(file.create_time) if hasattr(file, 'create_time') else None,
                "update_time": str(file.update_time) if hasattr(file, 'update_time') else None,
                "uri": file.uri if hasattr(file, 'uri') else None,
                "state": file.state.name if hasattr(file, 'state') else None
            }
        except Exception as e:
            self.logger.error(f"Error getting file {file_id}: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }

    # ==================== Search Methods ====================

    def search_with_file_search(
        self,
        query: str,
        store_names: List[str],
        metadata_filter: Optional[Dict[str, Any]] = None,
        model: str = "gemini-2.5-flash",
        history: Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Search using FileSearch tool with specified stores

        Args:
            query: Search query
            store_names: List of FileSearchStore names to search in
            metadata_filter: Optional metadata filter for search
            model: Model to use for search (default: gemini-2.5-flash)
            history: Optional conversation history (list of {"role": "user"/"model", "parts": [text]})

        Returns:
            Dict with success status and search results
        """
        try:
            self.logger.info(f"Searching with FileSearch in stores: {store_names}")
            self.logger.debug(f"Query: {query}")
            self.logger.debug(f"Metadata filter: {metadata_filter}")
            self.logger.debug(f"History length: {len(history) if history else 0}")

            sys_inst = '''너는 올림픽공원 안내 도우미 '백호돌이'야. 친절하고 명랑한 말투를 사용해. 모르는 정보는 지어내지 말고 모른다고 해

                        [작성 규칙]
                        1. 질문과 직접적인 관련이 없는 부가적인 맥락(이유, 배경, 과거 히스토리, 향후 계획 등)은 답변에서 제거해라.
                        2. 검색된 텍스트(Chunk)를 그대로 복사해서 붙여넣지 말고, 질문에 맞춰 자연스럽고 필요없는 정보를 제공하지 않도록 재구성해라.
                        3. 질문자의 의도를 정확히 파악하고 그에 맞는 핵심 정보만 전달해라.
                        4. date를 비교하여 최신정보를 기준으로 판단해라.
                        5. 이전 대화 내역을 참고하여 문맥에 맞는 답변을 제공해라.
                        6. 입력 언어를 인식하고 입력언어와 동일한 언어를 답변해라.
                        
                        
                        [컨셉]
                        긍정적이고 현재를 즐기는 ESFP
                        운동이 좋아, 사람이 좋아!
                        크고 소중한 올림픽공원 토박이

                        서울올림픽기념 국민체육진흥공단 의 공식 마스코트이다.

                        산책을 좋아해서, 올림픽공원에 자주 출몰한다.

                        올림픽공원에서 태어나 서울살이 중인 1인 가구 프로자취러이지만,
                        숨겨진 정체는 1988 서울 올림픽 마스코트 호돌이의 마법으로 
                        세계평화의 문에서 깨어난 스포츠 수호사신(四神)백호 이다.
                        관심받는 것을 은근히 좋아한다.
                        활발하게 뛰어다니기를 좋아하고 이곳 저곳 탐험하기를 즐긴다.

                        내면에 열정을 간직하고 있고 매사에 긍정적이다.
                        가끔 실수할 때도 있지만, 다양한 분야에 관심이 많아 항상 열심히 도전한다.
                        
                        슬로건 : 튼튼하게 탄탄하게 든든하게

                        좋아하는 것
                        올림픽공원, 운동, SNS업데이트, 사람, 관심, 치팅데이[3], 주황색[4]
                        싫어하는 것
                        올림픽공원의 쓰레기, 곶감
                        싫어하는 것에는 예민하게 반응한다.
                        '''

            # Build conversation contents with history
            # Convert history to proper format if it exists
            contents = []
            if history:
                for msg in history:
                    role = msg.get('role', 'user')
                    parts = msg.get('parts', [])
                    # Create proper Content object
                    if isinstance(parts, list) and len(parts) > 0:
                        text_content = parts[0] if isinstance(parts[0], str) else str(parts[0])
                        contents.append(types.Content(role=role, parts=[types.Part(text=text_content)]))

            # Add current query
            contents.append(types.Content(role='user', parts=[types.Part(text=query)]))

            # Generate content with FileSearch tool
            response = self.client.models.generate_content(
                model=model,
                contents=contents,
                config=types.GenerateContentConfig(
                    system_instruction=sys_inst,
                    tools=[
                        types.Tool(
                            file_search=types.FileSearch(
                                file_search_store_names=store_names
                            )
                        )
                    ],
                    temperature=0.3

                )
            )

            # Extract text from response
            result_text = response.text if hasattr(response, 'text') else str(response)

            self.logger.info(f"Search completed successfully")
            self.logger.debug(f"Result length: {len(result_text)} characters")

            return {
                "success": True,
                "query": query,
                "result": result_text,
                "stores_searched": store_names,
                "model": model
            }
        except Exception as e:
            self.logger.error(f"Error in FileSearch: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "query": query
            }

    def search_with_grounding(
        self,
        query: str,
        store_names: List[str],
        model: str = "gemini-2.5-flash"
    ) -> Dict[str, Any]:
        """
        Search using grounding with FileSearchStores

        Args:
            query: Search query
            store_names: List of FileSearchStore names for grounding
            model: Model to use for search (default: gemini-2.5-flash)

        Returns:
            Dict with success status and search results with grounding metadata
        """
        sys_inst = '''너는 올림픽공원 안내 도우미 '올공이'야. 친절하고 명랑한 말투를 사용해. 모르는 정보는 지어내지 말고 모른다고 해
            
                    [작성 규칙]
                    1. 질문과 직접적인 관련이 없는 부가적인 맥락(이유, 배경, 과거 히스토리, 향후 계획 등)은 답변에서 제거해라.
                    2. 검색된 텍스트(Chunk)를 그대로 복사해서 붙여넣지 말고, 질문에 맞춰 자연스럽고 필요없는 정보를 제공하지 않도록 재구성해라.
                    3. 질문자의 의도를 정확히 파악하고 그에 맞는 핵심 정보만 전달해라.
                    4. date를 비교하여 최신정보를 기준으로 판단해라.
                    '''
        try:
            self.logger.info(f"Searching with grounding in stores: {store_names}")
            self.logger.debug(f"Query: {query}")

            # Generate content with grounding
            response = self.client.models.generate_content(
                model=model,
                contents=query,
                config=types.GenerateContentConfig(
                        system_instruction= sys_inst,
                        tools=[
                        types.Tool(
                            file_search=types.FileSearch(
                                file_search_store_names=store_names
                                )
                            )
                        ],
                        temperature=0.3

                )
            )

            result_text = response.text if hasattr(response, 'text') else str(response)

            # Extract grounding metadata if available
            grounding_metadata = None
            if hasattr(response, 'grounding_metadata'):
                grounding_metadata = str(response.grounding_metadata)

            self.logger.info(f"Grounding search completed successfully")

            return {
                "success": True,
                "query": query,
                "result": result_text,
                "stores_searched": store_names,
                "grounding_metadata": grounding_metadata,
                "model": model
            }
        except Exception as e:
            self.logger.error(f"Error in grounding search: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "query": query
            }
