# Face-recognition-Attendance-System-Project


## 🍀 프로젝트 소개
- 프로젝트 기간: 2023.08.21(월) ~ 2023.09.02(토) / 13일
- 프로젝트명: 머신러닝과 딥러닝 활용한 인공지능 활용 프로젝트
- 프로젝트 목적: 작성예정
  -  머신러닝과 딥러닝을 활용하여 인공지능 프로그램을 개발할 수 있는 능력을 기른다.
  -  인공지능 프로그램을 개발함으로써 AI에 대한 이해도를 향상시킨다.
  -  원시 데이터를 가공 및 활용하는 능력을 기른다.



## 🖥️ 개발 환경
- 운영체제: Window 10 64 bit
- 개발언어: Python 3.11
- 개발 툴: Pycharm
- DBSM: PostgreSQL
- 추가 패키지: Pandas, Matplotlib, Sklearn, Tensorflow

  
## 📌 주요 기능
- 사원 모드
  - 얼굴 인식으로 프로그램을 로그인 / 출근 시간을 DB에 저장한다.
  - 로그인하면 홈페이지에서 해당 월의 출근일 / 결근일 / 출석률을 확인할 수 있다.
  - 외출/퇴근 복귀시 얼굴 인식을 통해 복귀할 수 있다.
  - 퇴근 시간은 DB에 저장된다.
  - 상단 메뉴에서 마이페이지를 클릭하여 내 사원 정보를 확인할 수 있다.
  - 수정하기 버튼을 클릭하여 비밀번호를 수정할 수 있다.
  - 수정된 비밀번호는 DB에 저장된다.

- 관리자 모드
  - 관리자 계정(admin)을 통해 관리자 전용 페이지로 로그인 할 수 있다.
  - 관리자 전용 홈페이지에는 부서 정보 조회 테이블, 부서별 근태율 / 부서별 인원 그래프를 확인 할 수 있다.
  - 사원 등록 버튼을 클릭하여 사원 정보를 입력, 얼굴 등록 후 신규 사원 등록이 가능하다.
  - 부서 정보 조회 테이블에서 각 column을 클릭하면 해당 row의 부서의 팀원을 확인할 수 있는 화면으로 이동한다.
  - 부서 이름을 선택할 수 있는 콤보박스에서 부서를 고른 후 확인을 누르면 해당 팀원을 확인할 수 있다.
  - 팀원 위젯 X 키를 눌러 사원 삭제를 할 수 있다.
  - 팀원 위젯을 클릭하면 해당 사원의 월간 근태를 확인할 수 있다.
  - 사원 정보 확인 버튼을 클릭하면 사원 정보가 담긴 다이얼로그가 디스플레이된다.
  - 관리자는 해당 사원의 부서를 변경할 수 있다. 변경 시 DB에 저장된다.
- 데이터 시각화:
  - 각 사원은 해당월 근태를 그래프로 확인할 수 있다.
  - 각 사원은 1 ~ 12월 근태를 그래프로 확인할 수 있다.
  - 각 사원은 해당월의 근무시간을 요약으로 확인할 수 있다.
  - 각 사원은 해당원의 근무시간을 확인할 수 있다.
  - 관리자는 각 부서별 월 평균 근태율을 그래프로 확인할 수 있다.
  - 관리자는 각 부서별 1 ~ 12월 평균 근태율을 그래프로 확인할 수 있다.
  - 관리자는 각 부서별 부서인원을 그래프로 확인할 수 있다.

## 🔍 시연 사진

1. 로딩 화면
<img width="100%" src="https://github.com/guaba98/Face-recognition-Attendance-System-Project/assets/121913371/1674e422-87f5-4c33-b160-2430ef4c484b"/>

2. 오픈 화면
<img width="100" src="https://github.com/guaba98/Face-recognition-Attendance-System-Project/assets/121913371/16381094-a10c-44e0-b186-1da083be283f"/>

3. 로그인 화면
<img width="100" src="https://github.com/guaba98/Face-recognition-Attendance-System-Project/assets/121913371/a3c57161-ad09-4674-bdbd-349723063159"/>
![3  외출 화면](https://github.com/guaba98/Face-recognition-Attendance-System-Project/assets/121913371/0fa5f099-a580-4281-9ad4-6dfe4ba6aec5)

5. 아이디, 비밀번호 입력하지 않았을 때
<img width="100" src="https://github.com/guaba98/Face-recognition-Attendance-System-Project/assets/121913371/b2d0863e-9501-4b62-b8f0-2205965ae630"/>

6. 로그인 성공시 메세지창
<img width="100" src="https://github.com/guaba98/Face-recognition-Attendance-System-Project/assets/121913371/08aaf148-00c3-4bad-8738-cad55802d1a0"/>

7. 메인화면
<img width="100" src="https://github.com/guaba98/Face-recognition-Attendance-System-Project/assets/121913371/71163ee3-57e0-493d-bdd3-8fcdc557780c"/>

8. 근무시간 그래프 클릭시 해당 달 근무시간 그래프 출력
<img width="100" src="(https://github.com/guaba98/Face-recognition-Attendance-System-Project/assets/121913371/b754e6ff-bd78-40ee-af81-0227e21f4b6c"/>

9. 월별 출근율 그래프 클릭시
<img width="100" src="https://github.com/guaba98/Face-recognition-Attendance-System-Project/assets/121913371/fdd26922-d921-456d-b13a-e3b90fe5fbb4"/>

8. 근태화면 페이지
<img width="100" src="https://github.com/guaba98/Face-recognition-Attendance-System-Project/assets/121913371/52189889-c6df-4d69-b66a-1b1946260205"/>

9. 근태화면 월별조회
<img width="100" src="https://github.com/guaba98/Face-recognition-Attendance-System-Project/assets/121913371/696888d1-6be5-46f9-b90c-db0f70c7e7f0"/>

10. 마이페이지
<img width="100" src="https://github.com/guaba98/Face-recognition-Attendance-System-Project/assets/121913371/ee8f5807-0c35-455f-94a7-b1fe63355d34"/>

11. 마이페이지 - 비밀번호 변경
<img width="100" src="https://github.com/guaba98/Face-recognition-Attendance-System-Project/assets/121913371/2d657a57-3a85-4543-9ff8-5c369783aba3"/>

12. 외출여부 질문
<img width="100" src="https://github.com/guaba98/Face-recognition-Attendance-System-Project/assets/121913371/e12f563a-f1a4-402f-82ba-bf30acd35a8b"/>



