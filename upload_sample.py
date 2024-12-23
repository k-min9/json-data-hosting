import requests
import json
import os
import base64
from dotenv import load_dotenv

load_dotenv()

# 업로드 예제 (파일 이름을 입력받아 업로드)
def upload_json(url, filename, token):
    # JSON 파일을 열고 내용 읽기
    if not os.path.exists(filename):
        print(f"{filename} 파일이 존재하지 않습니다.")
        return
    
    with open(filename, 'r') as file:
        data = json.load(file)

    # 파일 내용을 Base64로 인코딩
    encoded_content = base64.b64encode(json.dumps(data).encode('utf-8')).decode('utf-8')

    headers = {
        'Authorization': f'token {token}',
        'Content-Type': 'application/json'
    }

    # GitHub API로 PUT 요청 (업로드)
    payload = {
        "message": "Upload JSON file",
        "content": encoded_content,
        "branch": "master"
    }
    
    # GitHub API에서 해당 파일이 존재하는지 확인
    file_url = f"https://api.github.com/repos/k-min9/json-data-hosting/contents/upload.json?ref=master"
    response = requests.get(file_url, headers=headers)

    # 기존 파일이 있으면 sha 값을 사용하여 업데이트, 없으면 새로 생성
    if response.status_code == 200:
        # 파일이 이미 존재하므로 sha 값을 가져옴
        file_data = response.json()
        sha = file_data['sha']
        payload = {
            "message": "Update JSON file",
            "content": encoded_content,
            "sha": sha,
            "branch": "master"
        }
    else:
        # 파일이 없으면 새로 생성
        payload = {
            "message": "Upload JSON file",
            "content": encoded_content,
            "branch": "master"
        }

    # 파일 업로드 (혹은 업데이트)
    upload_response = requests.put(url, headers=headers, data=json.dumps(payload))

    if upload_response.status_code == 201 or upload_response.status_code == 200:
        print("Upload Success!")
    else:
        print(f"Upload Failed! Status Code: {upload_response.status_code}, Response: {upload_response.text}")


# 다운로드 예제
def download_json(url):
    response = requests.get(url)
    if response.status_code == 200:
        print("Download Success!")
        return response.json()
    else:
        print(f"Download Failed! Status Code: {response.status_code}")
        return None

if __name__ == '__main__':
    # 사용 예제
    upload_url = "https://api.github.com/repos/k-min9/json-data-hosting/contents/upload2.json"  # 업로드 URL (GitHub API를 사용)
    download_url = "https://raw.githubusercontent.com/k-min9/json-data-hosting/master/upload2.json"  # GitHub Pages 다운로드 URL

    # 사용자로부터 입력 받기
    token = os.getenv("GITHUB_TOKEN")
    filename = 'my_little_jarvis_plus_ngrok_server.json'

    # 업로드 테스트
    upload_json(upload_url, filename, token)

    # 다운로드 테스트
    downloaded_data = download_json(download_url)
    print("Downloaded Data:", downloaded_data)
