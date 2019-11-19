# How to deploy

## 1. Build EXE file

./bin/build_scraper.sh

## 2. Prerequisites

- Python 3 설치. (설치 마지막 화면에서 Disable path limit 여부 물어보는데 반드시 클릭하여 파일명 길이 제한 해제)

- InfoTech 모듈이 설치 되어있는지 확인 -> 프로그램 추가/제거에서 확인 가능

- default.json 에 설정된 path 가 실제 공인 인증서의 경로인지 확인 -> 일치하지 않을경우 default.json 의 관련부분 수정

## 3. Deploy

./enote_scraper/dist 에 위치한 kross_scraper.exe 를 실행

# Usage

- HTTP REST API 를 통해 외부에서 호출
    - method: POST
    - Port: 3001
    - Path: /enote/fetch
    - Content-type: application/json

- JSON 입력형식 parameter

| 항목 | 필수여부 또는 디폴트값 |
|----|----|
| appCd | "kross_scraper.exe" |
| orgCd | "unote" |
| svcCd | **필수** |
| loginMethod | "CERT" |
| signCert | "" |
| signPri | "" |
| signPw | "" |
| userId | "" |
| userPw | "" |
| bankCd | "ALL" |
| acctNo | "" |
| billNo | "" |
| detail | "Y" |
| fromDate | YYYYMMDD 형식. 생략시 (1년+15일) 전으로 지정 |
| toDate | YYYYMMDD 형식. 생략시 오늘자로 지정 |

- 날짜 지정시 유의 사항
    fromDate, toDate 값을 모두 지정하거나 아예 생략해야함. (하나만 지정시 에러)

- svcCd 유효 입력값

| svcCd | 분류  | 세부 분류
|------ |:-----:|-----:|
| B0001 | 발행어음 | 미지급제시
| B0011 | 발행어음 | 결제 어음
| B0021 | 발행어음 | 부도 어음
| B1001 | 배서어음 | 배서한 어음
| B1011 | 배서어음 | 배서받은 어음
| B2001 | 보유어음 | 결제받을 어음
| B2011 | 보유어음 | 결제받은 어음
| B2021 | 보유어음 | 부도어음
| B3001 | 보증어음 | 발행보증 어음
| B3011 | 보증어음 | 배서보증 어음
| B4001 | 반환어음 | 반환 어음
| B5001 | 수령거부어음 | 수령거부 어음
| B6001 | 부도반환어음 | 부도반환 어음
| B0101 | 확인서 | 부도확인서

- 같은 폴더 내에 생성되는 log 파일을 통해 프로그램의 현재 status 에 대해 확인

- 공인인증서의 이슈로 Windows 에서만 동작

- 실행 파일을 여러번 실행할 경우, 한번만 실행됨. (단, 여러 pc에서 동시에 돌리는 경우는 확인 불가)


##### Example format for JSON
```
{
	"appCd": "kross_scraper.exe",
	"orgCd": "unote",
	"svcCd": "B2021",
	"loginMethod": "CERT",
	"signCert": "",
	"signPri": "",
	"signPw": "",
	"userId": "",
	"userPw": "",
	"bankCd": "ALL",
	"acctNo": "",
	"billNo": "",
	"detail": "Y",
	"fromDate": "",
	"toDate": ""
}
```

## 공인 인증서 비밀번호 변경시

- 새로운 비밀번호의 암호화를 위해 아래 경로의 shell script 실행
./bin/encrypt_pw.sh

- 예시

sh encrypt_pw.sh --text newPassword123

The encrypted text is shown below.

gP9jOzA75VyIW6FRuHZimQcLB1rCTKpGN8hdEXw0eY3kMx

- 생성된 암호키를 default.json 파일의 "signPw" 항목에 업데이트
