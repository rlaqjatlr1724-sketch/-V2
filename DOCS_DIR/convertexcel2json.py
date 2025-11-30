# batch_convert.py
import pandas as pd
import json
import os
from pathlib import Path


def batch_convert_to_json(input_dir, output_dir):
    """폴더 안의 모든 엑셀/CSV 파일을 JSON으로 변환"""

    # 출력 디렉토리 생성
    os.makedirs(output_dir, exist_ok=True)

    # 지원하는 파일 확장자
    extensions = ['.csv', '.xlsx', '.xls']

    converted_files = []

    for file_path in Path(input_dir).iterdir():
        if file_path.suffix in extensions:
            try:
                # 파일 읽기
                if file_path.suffix == '.csv':
                    df = pd.read_csv(file_path, encoding='utf-8-sig')
                else:
                    df = pd.read_excel(file_path)

                # NaN 처리
                df = df.fillna('')

                # JSON 변환
                data = df.to_dict('records')

                # 출력 파일명
                output_file = os.path.join(output_dir, f"{file_path.stem}.json")

                # 저장
                with open(output_file, 'w', encoding='utf-8') as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)

                converted_files.append({
                    'input': str(file_path),
                    'output': output_file,
                    'records': len(data)
                })

                print(f"✅ {file_path.name} → {output_file} ({len(data)}개 레코드)")

            except Exception as e:
                print(f"❌ {file_path.name} 변환 실패: {str(e)}")

    print(f"\n🎉 총 {len(converted_files)}개 파일 변환 완료!")
    return converted_files


# 사용
if __name__ == "__main__":
    batch_convert_to_json('./input_csv', './output_json')