import os
from haralyzer import HarParser
import json
import pandas as pd

# HAR 파일 처리 함수
def process_har_file(har_file_path, output_excel_path):
    # HAR 파일 읽기
    with open(har_file_path, 'r', encoding='utf-8') as f:
        har_parser = HarParser(json.loads(f.read()))

    # .mp4 및 .MOV 요청 필터링 및 로드 속도, 파일 사이즈 추출
    mp4_requests = []
    for page in har_parser.pages:
        for entry in page.entries:
            # 요청 URL에 '.mp4' 또는 '.MOV'가 포함된 경우 필터링
            if '.jpg' in entry['request']['url'] or '.png' in entry['request']['url']:
                mp4_requests.append({
                    "URL": entry['request']['url'],
                    "Load Time (ms)": entry['timings']['receive'],  # 로드 속도 (ms 단위)
                    "File Size (bytes)": entry['response']['content']['size']  # 파일 사이즈 (bytes)
                })

    # 데이터프레임 생성
    df = pd.DataFrame(mp4_requests)

    # 결과 출력
    print(f"Total MP4/MOV requests found in {har_file_path}: {len(mp4_requests)}")
    print(df)

    # MP4 요청을 엑셀 파일로 저장
    df.to_excel(output_excel_path, index=False)
    print(f"MP4/MOV requests have been saved to {output_excel_path}")

# 디렉토리 내 파일들 순차적으로 처리하는 함수
def process_files_in_directory(directory_path):
    # 디렉토리 내 파일들 가져오기
    files = [f for f in os.listdir(directory_path) if os.path.isfile(os.path.join(directory_path, f))]

    # 파일이 존재하지 않을 경우
    if not files:
        print(f"No files found in the directory: {directory_path}")
        return

    # 각 HAR 파일을 순차적으로 처리
    for file_name in files:
        if file_name.endswith('.har'):  # HAR 파일만 처리
            har_file_path = os.path.join(directory_path, file_name)
            output_excel_path = os.path.join(directory_path, file_name.replace('.har', '(image).xlsx'))
            print(f"Processing HAR file: {har_file_path}")

            # HAR 파일 처리
            process_har_file(har_file_path, output_excel_path)

# 함수 호출
directory_path = "C:/workspace(etc)/haralyzer/venv/har-files"
process_files_in_directory(directory_path)
