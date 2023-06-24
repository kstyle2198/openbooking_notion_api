import os
import pandas as pd
import requests
import streamlit as st

NOTION_TOKEN = st.secrets['NOTION_TOKEN']
DATABASE_ID = st.secrets['DATABASE_ID']

headers = {
    "Authorization": f"Bearer {NOTION_TOKEN}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def get_pages(num_pages=None):
    """
    If num_pages is None, get all pages, otherwise just the defined number.
    """
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)

    data = response.json()

    # Comment this out to dump all data to a file
    # import json
    # with open('db.json', 'w', encoding='utf8') as f:
    #    json.dump(data, f, ensure_ascii=False, indent=4)

    results = data["results"]
    while data["has_more"] and get_all:
        payload = {"page_size": page_size, "start_cursor": data["next_cursor"]}
        url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
        response = requests.post(url, json=payload, headers=headers)
        data = response.json()
        results.extend(data["results"])

    return results


def check_duplicate(booking_date: str, table_number: str):
    
    target = get_pages()
    df = read_as_df(target)
    check1 = df.loc[(df["booking_date"]==booking_date)&(df["table_number"]==str(table_number))]["고유번호"].values
    
    if len(check1) == 0:
        return True
    
    else:
        return False



def insert_data(data: dict, booking_date, table_number):
    
    if check_duplicate(booking_date, table_number):
        url = 'https://api.notion.com/v1/pages'
        payload = {"parent": {"database_id": DATABASE_ID}, "properties": data}
        # print(f"payload: {payload}")
        res = requests.post(url, json=payload, headers=headers)
        print(f"response_status_code: {res.status_code}")
        # print(res.text)
        return True
    else:
        print("중복데이터 입력 오류")
        return False

# Function to handle booking deletion
def delete_booking(예약번호: int, 사번: str, booking_date: str):
    try:  
        target = get_pages()
        df = read_as_df(target)
        고유번호 = df.loc[(df["예약번호"] == int(예약번호))]["고유번호"].values[0]
        print(고유번호, df.loc[(df["고유번호"]==고유번호)]["사번"].values[0], df.loc[(df["고유번호"]==고유번호)]["booking_date"].values[0])
        
        if df.loc[(df["고유번호"]==고유번호)]["사번"].values[0] == 사번 and df.loc[(df["고유번호"]==고유번호)]["booking_date"].values[0] == booking_date:
            url = f"https://api.notion.com/v1/pages/{고유번호}"
            payload = {"archived": True}
            res = requests.patch(url, json=payload, headers=headers)
            print("해당 데이터 삭제 성공")
            return True
        
        else:
            print("해당 데이터가 없습니다.")
            return False
    except:
        print("에러 발생")
        return False

def read_as_df(target):
    pages = target
    예약번호_list, company_list, 사번_list, name_list, table_num_list, booking_date_list, status_list, 고유번호_list = [], [], [], [], [], [], [], []
    
    
    for page in pages:
        page_id = page["id"]
        props = page["properties"]
        
        예약번호 = props['예약번호']['unique_id']['number']
        company = props['company']['title'][0]['text']['content']
        사번 = props['사번']['rich_text'][0]['text']['content']
        name = props['name']['rich_text'][0]['text']['content']
        table_number =  props['table_number']['rich_text'][0]['text']['content']
        booking_date = props['booking_date']['rich_text'][0]['text']['content']
        status = props['status']['rich_text'][0]['text']['content']
        # 고유번호 = page["id"]
        # print(예약번호, company, 사번, name, table_number, booking_date, status, page_id)
        
        예약번호_list.append(예약번호)
        company_list.append(company)
        사번_list.append(사번)
        name_list.append(name)
        table_num_list.append(table_number)
        booking_date_list.append(booking_date)
        status_list.append(status)
        고유번호_list.append(page_id)
        df = pd.DataFrame(list(zip(예약번호_list, company_list, 사번_list, name_list, table_num_list, booking_date_list, status_list, 고유번호_list)), 
                        columns=['예약번호', 'company', '사번', 'name', 'table_number', 'booking_date', 'status', '고유번호'])
    return df


if __name__ == "__main__":

    company = "HDX"
    사번 = "A422525"
    name = "홍길동"
    table_number = "1"
    booking_date = "2023-06-28"
    status = "booked"

    data = {
        "company" : {"title": [{"text": {"content": company}}]},
        "사번": {"rich_text": [{"text": {"content": 사번}}]},
        "name": {"rich_text": [{"text": {"content": name}}]},
        "table_number": {"rich_text": [{"text": {"content": table_number}}]},
        "booking_date":  {"rich_text": [{"text": {"content": booking_date}}]},
        "status":  {"rich_text": [{"text": {"content": status}}]},
        }


    # insert_data(data)
    # delete_data("8a8017c4-1199-413f-9056-6c596a4ae211")

    
    # delete_booking("9f57977f-c713-4078-8cde-f87712454e1b", "A422525", "2023-06-29")
    target = get_pages()
    print(read_as_df(target))