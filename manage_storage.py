import os
import time
import logging
from datetime import datetime
from google import genai
from dotenv import load_dotenv

# 로깅 설정
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# .env 파일 로드 (환경 변수에 API 키가 설정되어 있어야 함)
load_dotenv()  # 프로젝트 루트의 .env 파일 로드
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    # config.py를 사용하는 경우를 위한 예외 처리
    try:
        import config

        api_key = config.GEMINI_API_KEY
    except (ImportError, AttributeError):
        print("API Key를 찾을 수 없습니다. .env 또는 config.py를 확인하세요.")
        exit()

# 클라이언트 초기화
client = genai.Client(api_key=api_key)


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title):
    print("\n" + "=" * 80)
    print(f" 🛠️  Gemini Storage Manager: {title}")
    print("=" * 80)


def list_stores():
    """1. 현재 존재하는 File Search Store(저장소) 목록 조회"""
    print_header("File Search Store 목록")
    try:
        stores = list(client.file_search_stores.list())
    except Exception as e:
        print(f"❌ 목록 조회 실패: {e}")
        return []

    if not stores:
        print("📭 생성된 저장소가 없습니다.")
        return []

    print(f"총 {len(stores)}개의 저장소가 발견되었습니다.\n")
    for idx, store in enumerate(stores):
        print(f" [{idx + 1}] 이름: {store.display_name}")
        print(f"     ID  : {store.name}")
        state = getattr(store, 'state', 'Active')
        print(f"     상태: {state}")
        print("-" * 60)

    return stores


def list_all_files():
    """2. 구글 클라우드(Gemini API)에 업로드된 모든 파일 조회"""
    print_header("업로드된 파일 목록 (File API)")
    print("※ 이름이 없는 파일은 업로드 시 display_name이 설정되지 않은 파일입니다.")
    print("※ 'ID'는 삭제 시 식별자로 사용됩니다.\n")

    try:
        files = list(client.files.list())
    except Exception as e:
        print(f"❌ 조회 실패: {e}")
        return []

    if not files:
        print("📭 업로드된 파일이 없습니다.")
        return []

    print(f"총 {len(files)}개의 파일이 발견되었습니다.\n")
    print(f"{'No':<4} | {'파일명 (Display Name)':<30} | {'파일 ID / URI':<35} | {'상태':<8}")
    print("-" * 90)

    for idx, f in enumerate(files):
        d_name = f.display_name if f.display_name else "(이름 없음)"
        file_id = f.name if f.name else "Unknown ID"
        state = f.state.name if f.state else "UNKNOWN"
        print(f"{idx + 1:<4} | {d_name[:28]:<30} | {file_id:<35} | {state:<8}")

    return files


def delete_store_menu():
    """3. 저장소 삭제 메뉴"""
    stores = list_stores()
    if not stores: return

    print("\n🗑️ 삭제할 저장소 번호를 입력하세요 (취소: 0)")
    try:
        choice = int(input("선택 > "))
        if choice == 0: return

        target = stores[choice - 1]
        confirm = input(f"⚠️ 정말로 저장소 '{target.display_name}'을(를) 삭제하시겠습니까? (y/n): ")

        if confirm.lower() == 'y':
            print("삭제 중...", end=" ")
            client.file_search_stores.delete(name=target.name)
            print("✅ 완료!")
            time.sleep(1)
    except (ValueError, IndexError):
        print("❌ 잘못된 입력입니다.")
        time.sleep(1)


def delete_file_menu():
    """4. 파일 삭제 메뉴 (전체 클라우드에서 삭제)"""
    files = list_all_files()
    if not files: return

    print("\n🗑️ 삭제할 파일 번호를 입력하세요")
    print("   - 개별 삭제: 번호 입력 (예: 1)")
    print("   - 전체 삭제: 999")
    print("   - 취소: 0")

    try:
        choice = int(input("선택 > "))
        if choice == 0: return

        if choice == 999:
            confirm = input("⚠️ 경고: 업로드된 '모든' 파일을 삭제하시겠습니까? 되돌릴 수 없습니다! (yes/no): ")
            if confirm.lower() == 'yes':
                print("삭제 시작...")
                for f in files:
                    try:
                        client.files.delete(name=f.name)
                        d_name = f.display_name if f.display_name else f.name
                        print(f"🗑️ 삭제됨: {d_name}")
                        time.sleep(0.5)
                    except Exception as e:
                        print(f"❌ 실패 ({f.name}): {e}")
                print("✅ 전체 삭제 완료")
            return

        target = files[choice - 1]
        d_name = target.display_name if target.display_name else target.name

        confirm = input(f"정말로 파일 '{d_name}'을(를) 영구 삭제하시겠습니까? (y/n): ")

        if confirm.lower() == 'y':
            client.files.delete(name=target.name)
            print(f"✅ 삭제 완료: {d_name}")
            time.sleep(1)

    except (ValueError, IndexError):
        print("❌ 잘못된 입력입니다.")
        time.sleep(1)


def manage_store_files_menu():
    """5. [NEW] 저장소 내부 파일 관리 (조회 및 삭제)"""
    stores = list_stores()
    if not stores: return

    print("\n관리할 저장소 번호를 선택하세요 (취소: 0)")
    try:
        store_choice = int(input("선택 > "))
        if store_choice == 0: return
        target_store = stores[store_choice - 1]
    except (ValueError, IndexError):
        print("❌ 잘못된 입력입니다.")
        time.sleep(1)
        return

    while True:
        clear_screen()
        print_header(f"저장소 관리: {target_store.display_name}")
        print("1. 📄 저장소 내부 파일 목록 조회")
        print("2. 🗑️  저장소에서 파일 제거 (연결 해제)")
        print("0. 🔙 뒤로 가기")
        print("-" * 60)

        sub_input = input("메뉴 선택 > ")

        if sub_input == '1':
            # 내부 파일 목록 조회
            print(f"\n📂 '{target_store.display_name}'에 연결된 파일 목록:")
            try:
                # File Search Documents API를 사용하여 저장소 내 문서 조회
                documents_iterator = client.file_search_stores.documents.list(parent=target_store.name)
                documents = []
                for doc in documents_iterator:
                    documents.append(doc)

                if not documents:
                    print("   (저장된 문서가 없습니다)")
                else:
                    print(f"   총 {len(documents)}개의 문서가 발견되었습니다.\n")
                    print(f"{'No':<4} | {'문서명 (Display Name)':<38} | {'생성 시간':<20} | {'상태':<10}")
                    print("-" * 90)

                    for idx, doc in enumerate(documents):
                        # 문서 이름 추출
                        d_name = "(이름 없음)"
                        if hasattr(doc, 'display_name') and doc.display_name:
                            d_name = doc.display_name
                        elif hasattr(doc, 'name'):
                            # name에서 파일명 추출 시도
                            doc_name_parts = doc.name.split('/')
                            if len(doc_name_parts) > 0:
                                d_name = doc_name_parts[-1]

                        # 생성 시간 추출 및 포맷팅
                        create_time = "알 수 없음"
                        if hasattr(doc, 'create_time') and doc.create_time:
                            try:
                                # RFC 3339 타임스탬프를 읽기 쉬운 형식으로 변환
                                # doc.create_time이 문자열인 경우
                                if isinstance(doc.create_time, str):
                                    dt = datetime.fromisoformat(doc.create_time.replace('Z', '+00:00'))
                                    create_time = dt.strftime('%Y-%m-%d %H:%M')
                                # 이미 datetime 객체인 경우
                                elif isinstance(doc.create_time, datetime):
                                    create_time = doc.create_time.strftime('%Y-%m-%d %H:%M')
                                else:
                                    # 기타 타임스탬프 객체
                                    create_time = str(doc.create_time)[:16]
                            except Exception as e:
                                logger.debug(f"시간 파싱 실패: {e}")
                                create_time = str(doc.create_time)[:16] if doc.create_time else "알 수 없음"

                        # 상태 확인
                        state = "ACTIVE"
                        if hasattr(doc, 'state'):
                            state = doc.state.name if hasattr(doc.state, 'name') else str(doc.state)

                        print(f"{idx + 1:<4} | {d_name[:36]:<38} | {create_time:<20} | {state:<10}")

                input("\n엔터를 누르면 메뉴로 돌아갑니다...")

            except AttributeError as e:
                logger.error(f"API 메서드 오류: {e}")
                logger.error(f"사용 가능한 메서드: {dir(client.file_search_stores)}")
                print(f"❌ Documents API 접근 실패: {e}")
                print(f"   Python SDK 버전을 확인하거나, 다른 메서드를 시도 중입니다...")

                # 대안: 다른 메서드 시도
                try:
                    # 저장소 상세 정보로 문서 수 확인
                    store_detail = client.file_search_stores.get(name=target_store.name)
                    logger.info(f"저장소 상세: {store_detail}")

                    print(f"\n   저장소 정보:")
                    if hasattr(store_detail, 'vector_search_stats'):
                        stats = store_detail.vector_search_stats
                        if hasattr(stats, 'num_documents'):
                            print(f"   - 연결된 문서 수: {stats.num_documents}개")

                    print(f"\n   ⚠️  개별 문서 목록 조회는 현재 SDK 버전에서 지원되지 않습니다.")
                    print(f"   💡 '2. 업로드된 파일 목록 확인' 메뉴를 사용하세요.")

                except Exception as e2:
                    logger.error(f"대안 방법도 실패: {e2}")
                    print(f"   대안 방법도 실패했습니다: {e2}")

                time.sleep(2)
            except Exception as e:
                logger.error(f"목록 조회 실패: {type(e).__name__} - {e}")
                print(f"❌ 목록 조회 실패: {e}")
                print(f"   디버깅 정보: {type(e).__name__}")
                time.sleep(2)

        elif sub_input == '2':
            # 파일 삭제 (연결 해제)
            print(f"\n🗑️ '{target_store.display_name}'에서 제거할 문서 번호를 입력하세요")
            print("   - 개별 제거: 번호 입력 (예: 1)")
            print("   - 전체 제거: 999")
            print("   - 취소: 0")
            try:
                # 저장소 내 문서 목록 조회
                documents_iterator = client.file_search_stores.documents.list(parent=target_store.name)
                documents = []
                for doc in documents_iterator:
                    documents.append(doc)

                if not documents:
                    print("   (제거할 문서가 없습니다)")
                    time.sleep(1)
                    continue

                # 문서 목록 표시
                print()
                for idx, doc in enumerate(documents):
                    d_name = "(이름 없음)"
                    if hasattr(doc, 'display_name') and doc.display_name:
                        d_name = doc.display_name
                    elif hasattr(doc, 'name'):
                        doc_name_parts = doc.name.split('/')
                        if len(doc_name_parts) > 0:
                            d_name = doc_name_parts[-1]

                    print(f"[{idx + 1}] {d_name}")

                del_choice = int(input("\n선택 > "))
                if del_choice == 0:
                    continue

                # 전체 삭제
                if del_choice == 999:
                    confirm = input(f"⚠️ 경고: 이 저장소의 '모든' 문서({len(documents)}개)를 제거하시겠습니까?\n   (청크를 포함한 모든 데이터가 삭제되며, 원본 파일은 유지됩니다)\n   정말로 실행하려면 'yes'를 입력하세요: ")
                    if confirm.lower() == 'yes':
                        print(f"\n제거 시작... (총 {len(documents)}개)")
                        success_count = 0
                        fail_count = 0

                        for idx, doc in enumerate(documents):
                            d_name = "(이름 없음)"
                            if hasattr(doc, 'display_name') and doc.display_name:
                                d_name = doc.display_name

                            try:
                                # force=True를 직접 전달하여 청크도 함께 삭제
                                client.file_search_stores.documents.delete(
                                    name=doc.name,
                                    force=True
                                )
                                print(f"🗑️ [{idx+1}/{len(documents)}] 제거됨: {d_name}")
                                success_count += 1
                                time.sleep(0.3)
                            except Exception as e:
                                print(f"❌ [{idx+1}/{len(documents)}] 실패 ({d_name}): {e}")
                                fail_count += 1
                                logger.error(f"문서 제거 실패 ({doc.name}): {e}")

                        print(f"\n✅ 전체 제거 완료: 성공 {success_count}개, 실패 {fail_count}개")
                        time.sleep(2)
                    else:
                        print("취소되었습니다.")
                        time.sleep(1)
                    continue

                # 개별 삭제
                if del_choice < 1 or del_choice > len(documents):
                    print("❌ 잘못된 번호입니다.")
                    time.sleep(1)
                    continue

                doc_to_remove = documents[del_choice - 1]

                # 문서명 다시 조회
                d_name = "(이름 없음)"
                if hasattr(doc_to_remove, 'display_name') and doc_to_remove.display_name:
                    d_name = doc_to_remove.display_name

                confirm = input(f"⚠️ '{d_name}' 문서를 이 저장소에서 제거하시겠습니까? (청크 포함, 원본 파일은 유지됨) (y/n): ")
                if confirm.lower() == 'y':
                    # Documents API를 사용하여 문서 삭제 (force=True를 직접 전달하여 청크도 함께 삭제)
                    client.file_search_stores.documents.delete(
                        name=doc_to_remove.name,
                        force=True
                    )
                    print("✅ 저장소에서 제거되었습니다.")
                    time.sleep(1)

            except AttributeError as e:
                logger.error(f"API 메서드 오류: {e}")
                print(f"\n⚠️  Documents API를 사용할 수 없습니다.")
                print(f"   대신: 메인 메뉴 > 4. 파일 삭제 (전체 클라우드에서)")
                time.sleep(2)
            except (ValueError, IndexError) as e:
                print("❌ 잘못된 입력입니다.")
                time.sleep(1)
            except Exception as e:
                logger.error(f"제거 실패: {type(e).__name__} - {e}")
                print(f"❌ 제거 실패: {e}")
                time.sleep(2)

        elif sub_input == '0':
            break
        else:
            print("잘못된 입력입니다.")
            time.sleep(0.5)


def main():
    while True:
        clear_screen()
        print_header("메인 메뉴")
        print("1. 📂 저장소(Store) 목록 확인")
        print("2. 📄 업로드된 파일(File) 목록 확인 (전체)")
        print("3. 🗑️  저장소 삭제")
        print("4. 🗑️  파일 삭제 (전체 클라우드에서)")
        print("5. 🏪 저장소 내부 파일 관리 (조회/삭제)")
        print("0. ❌ 종료")
        print("-" * 60)

        user_input = input("메뉴 선택 > ")

        if user_input == '1':
            list_stores()
            input("\n엔터를 누르면 메뉴로 돌아갑니다...")
        elif user_input == '2':
            list_all_files()
            input("\n엔터를 누르면 메뉴로 돌아갑니다...")
        elif user_input == '3':
            delete_store_menu()
        elif user_input == '4':
            delete_file_menu()
        elif user_input == '5':
            manage_store_files_menu()
        elif user_input == '0':
            print("프로그램을 종료합니다.")
            break
        else:
            print("잘못된 입력입니다.")
            time.sleep(0.5)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n종료합니다.")