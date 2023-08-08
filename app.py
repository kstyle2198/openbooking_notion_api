import streamlit as st
from datetime import datetime, date, timedelta
import pandas as pd
import numpy as np
import os
from notion_api import *
# from random_splash import img_requests, new_requests
import time

def date_range(start, end):
    start = datetime.strptime(start, "%Y-%m-%d")
    end = datetime.strptime(end, "%Y-%m-%d")
    dates = [date.strftime("%Y-%m-%d") for date in pd.date_range(start, periods=(end-start).days+1)]
    return dates

def download_df(name1):
    target = get_pages()
    df = read_as_df(target)
    if name1 != "":
        df = df[df["name"]==name1]
    return df

def display_df(name1):
    target = get_pages()
    df = read_as_df(target)
    df = df.drop("사번", axis=1)
    if name1 != "":
        df = df[df["name"]==name1]
    return df

def convert_df(df):
    return df.to_csv().encode('utf-8-sig')
     
# Main function
def main():
    st.set_page_config(page_title="🎈OpenBooking", page_icon="11", layout="wide")

    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown("#### :green[서울 계동 ] :blue[리모트 오피스] ")
        st.markdown('### 예약 프로그램 with Notion API 🎁')
        st.write('---')
        
        with st.expander("📢 ***주요 안내 사항***"):
            st.markdown("""
                    - 건설기계부문은 :blue[**10석**]을 배정받아 운영합니다. (사용 실적에 따라 조정)
                    - 미예약 테이블 현황에서 **숫자**가 예약 가능한 table_number 입니다.
                    - 좌석번호(table_number)는 :red[***날짜별 예약가능 T/O***]를 의미하며, 
                      실제 이용은 빈책상 임의 지정하여 사용하면 됩니다(완전자율좌석).
                    - Booking시 사번, 성명 정확히 입력 바랍니다. (HDX는 근태계도 상신 / 근태코드 : 리모트오피스)
                    - 동일 날짜에 1인이(동일 사번) 중복 예약 안됩니다.
                    - 리모트오피스 :blue[**위치, 출입, 식사**] 등 이용 관련 안내사항은 
                      사이드바 상단의 :green[노션 안내자료] 참고 바랍니다.
                    - 기타 이용상 문의사항은 메일로 연락 바랍니다.(yeongho.yun@hyundai-genuine.com)
                    """)
        
        
    # with col2:
        # topground_image = img_requests("sky")
        # topground_image = new_requests("sky")
        # st.image(topground_image, width=400, caption="random images from unsplash")


    # Menu selection
    menu_options = ['Add Booking', 'Delete Booking']
    with st.sidebar:
        st.header("🔅 **예약 및 취소는 사이드바에서!**")
        st.markdown("##### ***:green[📒 노션안내자료]*** : [link](https://www.notion.so/xitesolution/3e30de34864f4a478d7a67b05f5655d3?pvs=4)")
        menu_choice = st.sidebar.selectbox('🚀 **:blue[Select Menu]**', menu_options)
    
    # 예약 날짜 구간
    min_date = date.today()
    interval = timedelta(hours=360)  #예약가능구간 15일 부여
    max_date = min_date + interval
    
    # 본문
    
    tab1, tab2 = st.tabs(["🌻:blue[**예약자 리스트**]", "🍉:red[**미예약 테이블 현황**]"])

    with tab1:
    
        search_name = st.text_input("🔎 **이름으로 조회하기 (이름 입력후 엔터)**")
        st.dataframe(display_df(search_name), use_container_width=True)
        
        st.markdown("---")
        with st.expander(""): 
            csv = convert_df(download_df(search_name))
            뭘까 = st.text_input("🕵️‍♂️ 다운로드", type="password")
            download_key = os.getenv('download_key')

            if 뭘까 == download_key:
                val = False
            else: 
                val = True
            st.download_button(
            label="Download data as CSV",
            data=csv,
            file_name='download_df.csv',
            mime='text/csv', disabled=val
            )
 
    with tab2:       
        columns = date_range(min_date.strftime('%Y-%m-%d'), max_date.strftime('%Y-%m-%d')) 

        data = []
        for _ in columns:
            data.append(np.arange(1, 11))
        
        table_df = pd.DataFrame(data).T
        table_df.columns = columns    
        
        # 예약 좌석 체킹
        target = get_pages()
        df = read_as_df(target)

        df2 = df[["table_number", "booking_date", "name"]]
                
        for t_num, b_date in zip(df2["table_number"], df2["booking_date"]):
            for k in table_df.columns:
                # print(k, table_df[k])
                if b_date == k:
                    for val in table_df[k]:
                        if t_num == str(val):
                            num = int(val)-1
                            table_df[k].replace(table_df[k][num],"예약", inplace=True)
                        else:
                            pass
                else:
                    pass
        st.dataframe(table_df)
    


    if menu_choice == 'Add Booking':
        
        with st.sidebar:
            st.subheader('🐬 Add New Booking')
            company = st.selectbox('☘️ 소속 회사를 선택해주세요', ["HDX", "HDI", "HCE"])
            사번 = st.text_input('☘️ 사번을 입력해주세요')
            name = st.text_input('☘️ 성명을 입력해주세요(name)')
            table_number = st.selectbox("☘️ table_number를 입력해주세요", ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"])
            booking_date = st.date_input('📆 Booking Date', min_value=min_date, max_value=max_date)      
            status = "booked"
            data = {
                "company" : {"title": [{"text": {"content": company}}]},
                "사번": {"rich_text": [{"text": {"content": 사번}}]},
                "name": {"rich_text": [{"text": {"content": name}}]},
                "table_number": {"rich_text": [{"text": {"content": str(table_number)}}]},
                "booking_date":  {"rich_text": [{"text": {"content": str(booking_date)}}]},
                "status":  {"rich_text": [{"text": {"content": status}}]}
            }
            
            if st.button('🖍️ Submit Booking'):
                if len(사번) != 0 and len(name) != 0 and insert_data(data, str(사번), str(booking_date), str(table_number)[0]) == True:
                    insert_data(data, str(사번), str(booking_date), str(table_number)[1])

                else:
                    pass
                time.sleep(1)
                st.experimental_rerun()
                
    elif menu_choice == 'Delete Booking':
        
        with st.sidebar:
            st.subheader('🐼 Delete Booking')
            예약번호 = st.text_input('☘️ 예약번호')
            사번 = st.text_input("☘️ 사번")
            booking_date = str(st.date_input('📆 취소할 예약 날짜', min_value=min_date, max_value=max_date))
            
            if st.button('🗑️ Delete Booking') == True:
                delete_booking(예약번호, 사번, booking_date)
                print(delete_booking(예약번호, 사번, booking_date))
                time.sleep(1)
                st.experimental_rerun()
                
                           
    
    with st.sidebar:
        st.markdown("---")
        with st.expander("🔒 개인정보처리방침"):
            st.markdown('''
                        - 본 예약프로그램은 정식 예약프로그램 개발전까지 사용하는 임시 프로그램으로서, 본 프로그램상 수집하는 성명, 사번 등 개인정보는 회사의 개인정보관리규정에 따라 관리됩니다.                                           
                        ''')

if __name__ == "__main__":
        
    main()