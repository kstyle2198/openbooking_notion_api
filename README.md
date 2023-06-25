# openbooking_notion_api


![MarineGEO circle logo](/images/image1.png "MarineGEO logo")

- 예약 사이트 : [링크](https://openbooking.streamlit.app)

- 본 프로그램은 회사 리모트오피스 좌석 예약을 위한 것이며 정식 프로그램 개발전 이용자 편의를 돕기 위해 만든 임시 프로그램입니다.

- 초기 버전에서는 예약 데이터를 서버에 위치한 sqlite db에 저장했으나, streamlit 서버 특성상 일정 시간 접속이 없으면 app이 sleep 상태로 들어가고 reboot시 db가 초기화되는 문제가 발생하였습니다.

- 이에 DB를 Notion page로 만들고 Notion API를 사용하여 streamlit 서버 외부에 예약 데이터를 보관토록 방식을 변경하였습니다.

- 다소 이용 속도에 있어서 Notion DB를 사용하는 쪽이 느린 편이어서 이부분 아쉬움이 남습니다.

- 그래도 사용자가 동시다발적으로 빈 좌석을 확인하여 예약하고, 삭제하고 하는 기능에 있어서는 부족함이 없을 것으로 예상됩니다.

- 잘 사용하시길 바랍니다.

감사합니다.

*** 참고사항 ***
- clone하여 재사용시, .streamlit 폴더를 만들도 그 안에 secrets.toml 파일을 만들고 그 안에 id 등 저장후 사용 바랍니다. (자세한 사항은 Streamlit 문서 확인해주세요.)
