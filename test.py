import os
import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from page1 import MEF_graph, season_bar, season_MEF_bar,image_input
from page2 import predict_model, predict_model_graph
from page3 import optimize_data
from page3_sub import data_input1, data_input2, create_comparison_graph, create_comparison_graph1,MEF_comparison_graph


st.set_page_config(
    page_title="BCO2 건물 탄소관리 플랫폼",
    page_icon=":bar_chart:",
    initial_sidebar_state="expanded",
    layout="wide"
)

def set_page_style():
    st.markdown(
        """
        <style>
        .stApp {
            background-color: #ECEEF0;
            color: #30d3fc;
        }
        header, .css-18e3th9, .css-1b2w7b3 {
            background-color: #ECEEF0 !important;
        }
        .css-1d391kg {
            background-color: #000000 !important;
        }
        .css-1d391kg .element-container {
            color: #BBE2EC !important;
        }
        .css-1d391kg .stRadio, .css-1d391kg .stFileUploader, .css-1d391kg .stSelectbox, .css-1d391kg .stButton {
            color: #000000 !important;
        }
        .css-1d391kg h1, .css-1d391kg h2, .css-1d391kg h3, .css-1d391kg h4, .css-1d391kg h5, .css-1d391kg h6 {
            color: #BBE2EC !important;
        }
        .css-1d391kg .stMarkdown, .css-1d391kg .stTextInput, .css-1d391kg .stTextArea, .css-1d391kg .stCheckbox {
            color: #BBE2EC !important;
        }
        .css-1d391kg .stTabs {
            color: #000000 !important;
        }
        .css-1d391kg .stSlider {
            color: #000000 !important;
        }
        .css-1d391kg .stDataFrame {
            color: #000000 !important;
        }
        .css-1d391kg .stDateInput {
            color: #000000 !important;
        }
        [data-testid=stSidebar] {
            background-color: #BBC4CF;
            width: 150px;
        }
        .css-1y0tads {
            background-color: rgba(255, 255, 255, 0.1) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            color: #000000 !important;
        }
        .css-qbe2hs, .css-qbe2hs a, .css-qbe2hs button, .css-qbe2hs input, .css-qbe2hs label, .css-qbe2hs select, .css-qbe2hs textarea {
            color: #000000 !important;
        }
        .react-grid-layout {
            background-color: #000000 !important;
        }
        .react-draggable {
            background-color: #BBE2EC !important;
        }
        .react-grid-item {
            background-color: #000000 !important;
        }
        .react-resizable-handle {
            background-color: #000000 !important;
        }
        .scroll-container {
            overflow-y: auto;
            height: 100%;
        }
        .content-wrapper {
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }
        .graph-container {
            width: 100%;
            height: calc(100% - 50px);
        }
        .description {
            width: 100%;
            text-align: center;
            margin-top: 10px;
            flex-shrink: 0;
        }
        .title {
            resize: vertical;
            overflow: auto;
            background-color: #F1F8E9 !important;
        }
        .draggable {
            cursor: move;
            background-color: #F1F8E9 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

set_page_style()

# Initialize session state variables
if 'button_clicked' not in st.session_state:
    st.session_state.button_clicked = False
if 'default_file1' not in st.session_state:
    st.session_state.default_file1 = []
if 'default_file' not in st.session_state:
    st.session_state.default_file = pd.DataFrame()
if 'mef_paths' not in st.session_state:
    st.session_state.mef_paths = {}
if 'mef_data' not in st.session_state:
    st.session_state.mef_data = {}
if 'selected_year' not in st.session_state:
    st.session_state.selected_year = None
if 'energy_value_season' not in st.session_state:
    st.session_state.energy_value_season = pd.Series(dtype='float64')
if 'energy_value_total' not in st.session_state:
    st.session_state.energy_value_total = 0
if 'df_energy' not in st.session_state:
    st.session_state.df_energy = pd.DataFrame()
if 'predict_data' not in st.session_state:
    st.session_state.predict_data = pd.DataFrame()  # Initialize predict_data

# 현재 디렉토리 설정 및 이미지 경로
current_dir = os.path.dirname(__file__)
default_csv_path = os.path.join(current_dir, 'image', '2017.csv')  # Define default_csv_path here

# 사이드바 메뉴
with st.sidebar:
    image_html1 = image_input('메인로고.png','90%','100%','-10px','20px','center')
    if image_html1:
        st.markdown(image_html1, unsafe_allow_html=True)

    # 구분선 추가
    hr_color = '#FFFFFF'  # 구분선 색상 코드

    st.markdown(
        f"<hr style='border: 2.0px solid {hr_color}; margin-top: -10px; margin-bottom: -10px;'>",
        unsafe_allow_html=True)

    def set_button_style(encoded_image, width, height,margin_top,margin_bottom):
        st.markdown(
            f"""
            <style>
            .stButton > button {{
                height: {height};  /* 버튼 높이 조절 */
                width: {width};  /* 버튼 너비 조절 */
                background-image: url(data:image/png;base64,{encoded_image});  /* 버튼 배경 이미지를 설정 */
                background-size: contain;  /* 배경 이미지 크기를 버튼 크기에 맞춤 */
                background-position: center;  /* 배경 이미지 위치 중앙으로 */
                background-repeat: no-repeat;  /* 배경 이미지 반복 없음 */
                border: none;  /* 버튼 테두리 제거 */
                border-radius: 20px;  /* 버튼 테두리 둥글게 설정 */
                color: transparent;  /* 버튼 텍스트 투명하게 설정 */
                padding: 0;  /* 패딩 제거 */
                margin: 0;  /* 마진 제거 */
                margin-top: {margin_top};  /* 상단 간격 조절 */
                margin-bottom: {margin_bottom};  /* 상단 간격 조절 */

            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    st.write('')

    # 세션 상태 초기화
    if 'button_clicked' not in st.session_state:
        st.session_state.button_clicked = False
    image_encoded_html = image_input('클릭버튼.png', '100%', '100%', '0px', '0px', 'center')
    if image_encoded_html:
        encoded_image = image_encoded_html.split('base64,')[1].split('"')[0]
        set_button_style(encoded_image, '100%', '80px', '-50px','10px')

    if not st.session_state.button_clicked:
        use_default_csv = st.button('Click this!!')
        if use_default_csv:
            st.session_state.button_clicked = True  # Mark the button as clicked
            default_file = data_input1(default_csv_path) #과거
            predict_data = predict_model(default_csv_path) #예측
            st.session_state.predict_data = predict_data
            default_file['date'] = pd.to_datetime(default_file['date'])  # Ensure the 'date' column is in datetime format
            default_file1 = default_file['date'].dt.year.unique()
            default_file1 = sorted(default_file1, reverse=True)  # Sort in descending order

            st.session_state.default_file = default_file
            st.session_state.default_file1 = default_file1

            mef_path_주중_2022 = os.path.join(current_dir, 'image', 'MEF(2022)주중.csv')
            mef_path_주말_2022 = os.path.join(current_dir, 'image', 'MEF(2022)주말.csv')
            mef_path_주중_2021 = os.path.join(current_dir, 'image', 'MEF(2021)주중.csv')
            mef_path_주말_2021 = os.path.join(current_dir, 'image', 'MEF(2021)주말.csv')
            mef_path_주중_2020 = os.path.join(current_dir, 'image', 'MEF(2020)주중.csv')
            mef_path_주말_2020 = os.path.join(current_dir, 'image', 'MEF(2020)주말.csv')

            st.session_state.mef_paths = {
                '주중_2022': mef_path_주중_2022,
                '주말_2022': mef_path_주말_2022,
                '주중_2021': mef_path_주중_2021,
                '주말_2021': mef_path_주말_2021,
                '주중_2020': mef_path_주중_2020,
                '주말_2020': mef_path_주말_2020
            }

            st.session_state.mef_data = {
                '주중_2022': pd.read_csv(mef_path_주중_2022),
                '주말_2022': pd.read_csv(mef_path_주말_2022),
                '주중_2021': pd.read_csv(mef_path_주중_2021),
                '주말_2021': pd.read_csv(mef_path_주말_2021),
                '주중_2020': pd.read_csv(mef_path_주중_2020),
                '주말_2020': pd.read_csv(mef_path_주말_2020)
            }

    selected_option = option_menu(
        menu_title="",
        options=["대표 솔루션", "사후 솔루션 Detail", "미래 솔루션 Detail", "한계배출계수 Detail"],
        icons=["house", "bar-chart", "graph-up"],
        menu_icon="cast",
        default_index=0,
        orientation="vertical"
    )
    st.session_state.selected_option = selected_option  # Save selected option to session state

# The following block runs once to initialize session state values
# The following block runs once to initialize session state values
if 'initialized' not in st.session_state:
    if st.session_state.default_file1:
        selected_year = st.session_state.default_file1[0]  # Default to the first year if no year is selected
        selected_csv_path = st.session_state.default_file[st.session_state.default_file['date'].dt.year == selected_year]

        energy_Total_season = selected_csv_path.groupby('season')['powerusage'].sum()
        energy_Total_season = energy_Total_season.reindex(['봄', '여름', '가을', '겨울'])
        energy_value_total = energy_Total_season.sum()
        df_energy = optimize_data(st.session_state.mef_paths['주중_2022'], st.session_state.mef_paths['주말_2022'], selected_csv_path)
        st.session_state.energy_value_season = energy_Total_season  # 이 줄을 추가하여 세션 상태에 energy_value_season 저장
        st.session_state.selected_year = selected_year
        st.session_state.energy_value_total = energy_value_total
        st.session_state.df_energy = df_energy

        predict_data1 = data_input2(st.session_state.predict_data)
        st.session_state.predict_data1 = predict_data1  # Store predict_data1 in session state
        df_energy_predict = optimize_data(st.session_state.mef_paths['주중_2022'],
                                          st.session_state.mef_paths['주말_2022'], predict_data1)
        st.session_state.df_energy_predict = df_energy_predict
        st.session_state.initialized = True
title_color= "black"
hr_color = '#9da8ab'  # 구분선 색상 코드
text_color = 'black'  # 두 번째 텍스트 색상

if st.session_state.selected_option == "대표 솔루션":
    with st.container():
        image_html1 = image_input('효과설명3.png', '40%', '60%', '-25px', '15px', 'left')
        if image_html1:
            st.markdown(image_html1, unsafe_allow_html=True)

        # 구분선 추가
        st.markdown(
            f"<hr style='border: 2.0px solid {hr_color}; margin-top: 0px; margin-bottom: 0px;'>",
            unsafe_allow_html=True)

        # 스타일 정의
        st.markdown(
            f"""
            <style>
            .reduced-margin-1 {{
                margin-top: 0px;
                margin-bottom: 10px;
                padding-top: 0px;
                padding-bottom: 0px;
                line-height: 1.0;
                color: {text_color};
                font-size:20px;
                font-weight: bold;
            }}
            .reduced-margin-2 {{
                margin-top: 0px;
                margin-bottom: 50px;
                padding-top: 0px;
                padding-bottom: 0px;
                line-height: 1.0;
                color: {text_color};
                font-size: 20px;
                font-weight: bold;
            }}
            .con-margin {{
                margin-top: -20px;  /* 이 값을 조정하여 con1, con2, con3의 상단 간격을 줄일 수 있습니다. */
                margin-bottom: 0px;
                padding-top: 0px;
                padding-bottom: 0px;
            }}
            .centered {{
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
            }}
            .large-sub {{
                font-size: 0.6em; /* Adjust this value to change the size of the subscript */
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

        if not st.session_state.energy_value_season.empty:
            image_html1 = image_input('멘트1.png', '50%', '100%', '0px', '30px', 'left')
            if image_html1:
                st.markdown(image_html1, unsafe_allow_html=True)

            con1, con2 = st.columns([0.4, 0.4])

            with con1:
                data = st.session_state.df_energy_predict
                grouped_powerusage = data.groupby('날짜')['MEF_CO2'].sum()
                max_down_date = grouped_powerusage.idxmin()

                create_comparison_graph(data, max_down_date)

            with con2:
                con2_1, con2_2 = st.columns(2)

                with con2_1:
                    grouped_powerusage = data.groupby('날짜')['MEF_CO2'].sum()
                    max_down_date = grouped_powerusage.idxmin()
                    grouped_total = data[data['날짜'] == max_down_date]
                    grouped_total_value = grouped_total['MEF_CO2'].sum() * (-1)
                    grouped_total_value = grouped_total_value.round(0).astype(int)
                    st.markdown(
                        f"""
                        <div class='centered con-margin' style='margin-top: 0px; padding: 10px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #848484;'>
                            <h2 style='font-size:30px; color:#FFFFFF; font-weight: bold;'>일별 최대 절감량
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown(
                        f"""
                        <div class='centered con-margin' style='margin-top: 10px; padding: 30px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #FFFFFF; max-width: 100%; margin-left: auto; margin-right: auto;'>
                            <h2 style='font-size:70px; color:black; font-weight: bold;'>
                                {grouped_total_value} <span style='font-size:50px;'>kgCO<sub style='font-size: 40px;'>2</sub></span>
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                with con2_2:
                    data = st.session_state.df_energy_predict
                    cal_Total = (data['MEF_CO2'].sum()) * (-1)
                    cal_Total1 = cal_Total.round(0).astype(int)

                    st.markdown(
                        f"""
                        <div class='centered con-margin' style='margin-top: 0px; padding: 10px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #848484;'>
                            <h2 style='font-size:30px; color:#FFFFFF; font-weight: bold;'>다음달 총 절감량
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f"""
                        <div class='centered con-margin' style='margin-top: 10px; padding: 30px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #FFFFFF; max-width: 100%; margin-left: auto; margin-right: auto;'>
                            <h2 style='font-size:70px; color:black; font-weight: bold;'>
                                {cal_Total1}  <span style='font-size:50px;'>kgCO<sub style='font-size: 40px;'>2</sub></span>
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    cal_Total2 = cal_Total * 1000 / 74
                    cal_Total2 = cal_Total2.round(0).astype(int)
                    cal_Total3 = cal_Total / 8
                    cal_Total3 = cal_Total3.round(0).astype(int)

                st.markdown(
                    f"""
                    <div class='centered con-margin' style='margin-top: 20px; padding: 10px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #848484;'>
                        <h2 style='font-size:30px; color:#FFFFFF; font-weight: bold;'>다음달 절감 효과
                        </h2>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                con2_3, con2_4 = st.columns([0.2, 0.7])
                with con2_3:
                    st.write('')
                    image_html1 = image_input('차.png', '90%', '70%', '0px', '0px', 'center')
                    if image_html1:
                        st.markdown(image_html1, unsafe_allow_html=True)
                with con2_4:
                    st.markdown(
                        f"""
                        <div class='centered con-margin' style='margin-top: 15px; padding: 20px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #FFFFFF; max-width: 100%; margin-left: auto; margin-right: auto;'>
                            <h2 style='font-size:40px; color:black; font-weight: bold;'>자동차 주행거리<br>
                                <span style='font-size:60px;'>{cal_Total2}</span>
                                <span style='font-size:50px;'>km</span>
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                con2_5, con2_6 = st.columns([0.2, 0.7])
                with con2_5:
                    st.write('')
                    image_html1 = image_input('나무.png', '90%', '70%', '0px', '0px', 'center')
                    if image_html1:
                        st.markdown(image_html1, unsafe_allow_html=True)
                with con2_6:
                    st.markdown(
                        f"""
                        <div class='centered con-margin' style='margin-top: 20px; padding: 20px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #FFFFFF; max-width: 100%; margin-left: auto; margin-right: auto;'>
                            <h2 style='font-size:40px; color:black; font-weight: bold;'>식재 효과<br>
                                <span style='font-size:60px;'>{cal_Total3}</span>
                                <span style='font-size:40px;'>그루</span>
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            st.markdown(
                f"<hr style='border: 0.5px solid {hr_color}; margin-top: -40px; margin-bottom: 0px;'>",
                unsafe_allow_html=True)
            st.write(' ')
            df_energy_predict = st.session_state.df_energy_predict

            df_energy_Total = df_energy_predict['powerusage'].sum()
            df_energy_Total = df_energy_Total / 1000
            df_energy_Total = (df_energy_Total.round(0)).astype(int)

            selected_data_MEF = (df_energy_predict['MEF_CO2'].sum()) * (-1)
            selected_data_MEF_Total = selected_data_MEF.round(0).astype(int)

            st.markdown(
                f"""
                <div class='centered con-margin' style='margin-top:-60px; margin-bottom: 0px;'>
                    <h2 style='font-size:40px; color:black;'>
                        모델적용 시, 다음달 전기사용량은 <strong><span style='color:red;'>{df_energy_Total}</span> MWh</strong>정도이고, CO<sub class='large-sub'>2</sub>는 <strong><span style='color:red;'>{selected_data_MEF_Total}</span> kgCO<sub class='large-sub'>2</sub></strong> 절감될 것으로 예상됩니다.
                    </h2>
                </div>
                """,
                unsafe_allow_html=True
            )
            st.write(' ')

            st.markdown(
                f"<hr style='border: 0.5px solid {hr_color}; margin-top: -20px; margin-bottom: -10px;'>",
                unsafe_allow_html=True)

        else:
            st.error("Please upload the CSV file by clicking the 'Click this!!' button.")
        st.markdown(
            f"<hr style='border: 2.0px solid {hr_color}; margin-top: -10px; margin-bottom: -10px;'>",
            unsafe_allow_html=True)




if st.session_state.selected_option == "사후 솔루션 Detail":
    with st.container():
        image_html1 = image_input('효과설명3.png', '40%', '60%', '-25px', '15px', 'left')
        if image_html1:
            st.markdown(image_html1, unsafe_allow_html=True)

        # 구분선 추가
        st.markdown(
            f"<hr style='border: 2.0px solid {hr_color}; margin-top: 0px; margin-bottom: 0px;'>",
            unsafe_allow_html=True)

        # 스타일 정의
        st.markdown(
            f"""
            <style>
            .reduced-margin-3 {{
                margin-top: 0px;
                margin-bottom: -10px;
                padding-top: 0px;
                padding-bottom: 0px;
                line-height: 1.0;
                color: {text_color};
            }}            
            .con-margin {{
                margin-top: -20px;  /* 이 값을 조정하여 con1, con2, con3의 상단 간격을 줄일 수 있습니다. */
                margin-bottom: 0px;
                padding-top: 0px;
                padding-bottom: 0px;
            }}
            .centered {{
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
            }}
            .large-sub {{
                font-size: 0.6em; /* Adjust this value to change the size of the subscript */
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
        if not st.session_state.energy_value_season.empty:
            image_html1 = image_input('멘트1.png', '50%', '100%', '0px', '30px', 'left')
            if image_html1:
                st.markdown(image_html1, unsafe_allow_html=True)

            st.markdown(
                f'<h2 style="font-size:24px; color:{title_color}; margin-top: 10px; margin-bottom: -10px; font-weight: bold;">1. 사후 최근연도 최적화 결과</h2>',
                unsafe_allow_html=True)
            st.markdown(
                f"<hr style='border: 0.5px solid {hr_color}; margin-top: -10px; margin-bottom: -10px;'>",
                unsafe_allow_html=True)
            data = st.session_state.df_energy

            con1, con2 = st.columns([0.4,0.8])
            with con1:
                con1_1, con1_2 = st.columns([0.5, 0.5])
                with con1_1:
                    energy_value_season=st.session_state.energy_value_season
                    energy_value_season=energy_value_season.round(0)

                    total = energy_value_season.sum()
                    total=(total/1000).astype(int)
                    st.markdown(
                        f"""
                        <div class='centered con-margin' style='margin-top: 0px; padding: 0px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #848484;'>
                            <h2 style='font-size:30px; color:#FFFFFF; font-weight: bold;'>연간 총 사용량
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f"""
                        <div class='centered con-margin' style='margin-top: 10px; padding:0px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #FFFFFF; max-width: 100%; margin-left: auto; margin-right: auto;'>
                            <h2 style='font-size:50px; color:black; font-weight: bold;'>
                                {total} MWh
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                with con1_2:

                    season_MEF=(data.groupby('season')['MEF_CO2'].sum())
                    season_MEF = season_MEF.reindex(['봄', '여름', '가을', '겨울']).reset_index()
                    season_MEF['MEF_CO2']=(season_MEF['MEF_CO2']*(-1))
                    season_MEF_total=season_MEF['MEF_CO2'].sum()
                    season_MEF_total1=(season_MEF_total).round(0).astype(int)

                    season_MEF_total2 = season_MEF_total * 1000 / 74
                    season_MEF_total2 = season_MEF_total2.round(0).astype(int)
                    season_MEF_total3 = season_MEF_total / 8
                    season_MEF_total3=season_MEF_total3.round(0).astype(int)


                    st.markdown(
                        f"""
                        <div class='centered con-margin' style='margin-top: 0px; padding: 0px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #848484;'>
                            <h2 style='font-size:30px; color:#FFFFFF; font-weight: bold;'>연간 총 절감량
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f"""
                        <div class='centered con-margin' style='margin-top: 10px; padding:0px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #FFFFFF; max-width: 100%; margin-left: auto; margin-right: auto;'>
                            <h2 style='font-size:50px; color:black; font-weight: bold;'>
                                {season_MEF_total1} kgCO<sub class='large-sub'>2</sub>
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                st.markdown(
                    f"""
                    <div class='centered con-margin' style='margin-top: 10px; padding: 0px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #848484;'>
                        <h2 style='font-size:30px; color:#FFFFFF; font-weight: bold;'>연간 절감 효과
                        </h2>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                con2_3,con2_4 = st.columns([0.3, 0.9])
                with con2_3:
                    st.write('')
                    image_html1 = image_input('차.png','70%','70%','0px','0px','center')
                    if image_html1:
                        st.markdown(image_html1, unsafe_allow_html=True)
                with con2_4:
                    st.markdown(
                        f"""
                        <div class='centered con-margin' style='margin-top: 10px; padding: 0px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #FFFFFF; max-width: 100%; margin-left: auto; margin-right: auto;'>
                            <h2 style='font-size:30px; color:black; font-weight: bold;'>자동차 주행거리<br>
                                <span style='font-size:40px;'>{season_MEF_total2}</span>
                                <span style='font-size:30px;'>km</span>
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                con2_5,con2_6 = st.columns([0.3, 0.9])
                with con2_5:
                    st.write('')
                    image_html1 = image_input('나무.png','70%','70%','0px','0px','center')
                    if image_html1:
                        st.markdown(image_html1, unsafe_allow_html=True)
                with con2_6:
                    st.markdown(
                        f"""
                        <div class='centered con-margin' style='margin-top: 10px; padding: 0px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #FFFFFF; max-width: 100%; margin-left: auto; margin-right: auto;'>
                            <h2 style='font-size:30px; color:black; font-weight: bold;'>식재 효과<br>
                                <span style='font-size:40px;'>{season_MEF_total3}</span>
                                <span style='font-size:30px;'>그루</span>
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

            with con2:
                predict_model_graph(data, width=1280, height=470)


            st.markdown(
                f'<h2 style="font-size:24px; color:{title_color}; margin-top: 10px; margin-bottom: -10px; font-weight: bold;">2. 계절별 사용량 및 절감량</h2>',
                unsafe_allow_html=True)
            st.markdown(
                f"<hr style='border: 0.5px solid {hr_color}; margin-top: -10px; margin-bottom: -10px;'>",
                unsafe_allow_html=True)
            data = st.session_state.df_energy
            data = data[['date','season', 'powerusage', 'optimized_powerusage', 'MEF_CO2']]
            data['날짜'] = data['date'].dt.date
            data['hour'] = data['date'].dt.hour

            con2, B, con3 = st.columns([0.5,0.05,0.5])


            with con2:
                season_bar(energy_value_season, width=900, height=480)

            with con3:
                season_MEF=(data.groupby('season')['MEF_CO2'].sum())
                season_MEF = season_MEF.reindex(['봄', '여름', '가을', '겨울']).reset_index()
                season_MEF['MEF_CO2']=(season_MEF['MEF_CO2']*(-1))
                season_MEF=season_MEF.round(0)
                season_MEF_bar(season_MEF, width=900, height=480)

            st.markdown(
                f'<h2 style="font-size:24px; color:{title_color}; margin-top: 10px; margin-bottom: -10px; font-weight: bold;">3. 일별 최적화 및 절감량</h2>',
                unsafe_allow_html=True)
            st.markdown(
                f"<hr style='border: 0.5px solid {hr_color}; margin-top: -10px; margin-bottom: -10px;'>",
                unsafe_allow_html=True)
            data = st.session_state.df_energy

            st.markdown("""
                <style>
                .stSelectbox div[data-baseweb="select"] > div {
                    background-color: white;
                }
                .stSelectbox {
                    margin-top: -20px;
                }
                </style>
                """, unsafe_allow_html=True)

            # 날짜 선택
            selected_date = st.selectbox('날짜를 선택하세요', data['날짜'].unique())

            # 선택된 데이터 필터링
            selected_data = data[data['날짜'] == selected_date]
            if not selected_data.empty:
                st.write(f"선택된 날짜: {selected_date}")

            con1, con2, con3 = st.columns([0.4,0.4,0.4])
            with con1:
                con1_1, con1_2 = st.columns([0.5, 0.5])
                with con1_1:
                    selected_data_power = (selected_data['optimized_powerusage'].sum())/1000
                    selected_data_power=selected_data_power.round(0).astype(int)

                    st.markdown(
                        f"""
                        <div class='centered con-margin' style='margin-top: 0px; padding: 0px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #848484;'>
                            <h2 style='font-size:30px; color:#FFFFFF; font-weight: bold;'>일별 총 사용량
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f"""
                        <div class='centered con-margin' style='margin-top: 10px; padding:0px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #FFFFFF; max-width: 100%; margin-left: auto; margin-right: auto;'>
                            <h2 style='font-size:50px; color:black; font-weight: bold;'>
                                {selected_data_power} MWh
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                with con1_2:

                    selected_data_MEF = (selected_data['MEF_CO2'].sum()) * (-1)
                    selected_data_MEF_Total = selected_data_MEF.round(0).astype(int)


                    selected_data_MEF_Total1 = selected_data_MEF_Total * 1000 / 74
                    selected_data_MEF_Total1 = selected_data_MEF_Total1.round(0).astype(int)
                    selected_data_MEF_Total2=selected_data_MEF_Total/8
                    selected_data_MEF_Total2 = selected_data_MEF_Total2.round(0).astype(int)


                    st.markdown(
                        f"""
                        <div class='centered con-margin' style='margin-top: 0px; padding: 0px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #848484;'>
                            <h2 style='font-size:30px; color:#FFFFFF; font-weight: bold;'>일별 총 절감량
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f"""
                        <div class='centered con-margin' style='margin-top: 10px; padding:0px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #FFFFFF; max-width: 100%; margin-left: auto; margin-right: auto;'>
                            <h2 style='font-size:50px; color:black; font-weight: bold;'>
                                {selected_data_MEF_Total} kgCO<sub class='large-sub'>2</sub>
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                st.markdown(
                    f"""
                    <div class='centered con-margin' style='margin-top: 10px; padding: 0px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #848484;'>
                        <h2 style='font-size:30px; color:#FFFFFF; font-weight: bold;'>일별 절감 효과
                        </h2>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

                con2_3,con2_4 = st.columns([0.3, 0.9])
                with con2_3:
                    st.write('')
                    image_html1 = image_input('차.png','70%','60%','0px','0px','center')
                    if image_html1:
                        st.markdown(image_html1, unsafe_allow_html=True)
                with con2_4:
                    st.markdown(
                        f"""
                        <div class='centered con-margin' style='margin-top: 10px; padding: 0px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #FFFFFF; max-width: 100%; margin-left: auto; margin-right: auto;'>
                            <h2 style='font-size:30px; color:black; font-weight: bold;'>자동차 주행거리<br>
                                <span style='font-size:40px;'>{selected_data_MEF_Total1}</span>
                                <span style='font-size:30px;'>km</span>
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                con2_5,con2_6 = st.columns([0.3, 0.9])
                with con2_5:
                    st.write('')
                    image_html1 = image_input('나무.png','70%','60%','0px','0px','center')
                    if image_html1:
                        st.markdown(image_html1, unsafe_allow_html=True)
                with con2_6:
                    st.markdown(
                        f"""
                        <div class='centered con-margin' style='margin-top: 10px; padding: 0px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #FFFFFF; max-width: 100%; margin-left: auto; margin-right: auto;'>
                            <h2 style='font-size:30px; color:black; font-weight: bold;'>식재 효과<br>
                                <span style='font-size:40px;'>{selected_data_MEF_Total2}</span>
                                <span style='font-size:30px;'>그루</span>
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )


                with con2:
                    create_comparison_graph1(selected_data, selected_date, width=600, height=470)

                with con3:
                    MEF_comparison_graph(selected_data, selected_date, width=600, height=470)


            st.markdown(
                f'<h2 style="font-size:24px; color:{title_color}; margin-top: 10px; margin-bottom: -10px; font-weight: bold;">4. 최적화 결과 파일 저장</h2>',
                unsafe_allow_html=True)
            st.markdown(
                f"<hr style='border: 0.5px solid {hr_color}; margin-top: -10px; margin-bottom: -10px;'>",
                unsafe_allow_html=True)
            data = st.session_state.df_energy

            st.markdown("<div class='reduced-margin-3'>  ↓↓↓  버튼을 누르면 아래 최적화 결과 파일을 출력할 수 있습니다.</div>", unsafe_allow_html=True)

            csv = data.to_csv(index=True).encode('utf-8-sig')

            # CSS와 HTML을 사용하여 버튼을 우측 정렬
            st.markdown("""
                <style>
                .download-button-container {
                    display: flex;
                    justify-content: flex-end;
                    margin-top: 0px; /* 버튼과 상단 컨텐츠 사이의 간격 조절 */
                }
                </style>
                <div class="download-button-container">
                """, unsafe_allow_html=True)

            st.markdown("""
                <div class="download-button-container">
                """, unsafe_allow_html=True)

            # 다운로드 버튼 생성
            st.download_button(
                label="CSV로 다운로드",
                data=csv,
                file_name='사후 최적화 결과.csv',
                mime='text/csv',
            )

            st.markdown("</div>", unsafe_allow_html=True)

            st.write(data)
        else:
            st.error("Please upload the CSV file by clicking the 'Click this!!' button.")
        st.markdown(
            f"<hr style='border: 2.0px solid {hr_color}; margin-top: -10px; margin-bottom: -10px;'>",
            unsafe_allow_html=True)




if st.session_state.selected_option == "미래 솔루션 Detail":
    with st.container():
        image_html1 = image_input('효과설명3.png', '40%', '60%', '-25px', '15px', 'left')
        if image_html1:
            st.markdown(image_html1, unsafe_allow_html=True)

        # 구분선 추가
        st.markdown(
            f"<hr style='border: 2.0px solid {hr_color}; margin-top: 0px; margin-bottom: 0px;'>",
            unsafe_allow_html=True)

        # 스타일 정의
        st.markdown(
            f"""
            <style>
            .reduced-margin-3 {{
                margin-top: 0px;
                margin-bottom: -10px;
                padding-top: 0px;
                padding-bottom: 0px;
                line-height: 1.0;
                color: {text_color};
            }}            
            .centered {{
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
            }}
            .large-sub {{
                font-size: 0.6em; /* Adjust this value to change the size of the subscript */
            }}
            </style>
            """,
            unsafe_allow_html=True
        )


        if 'predict_data1' in st.session_state:
            image_html1 = image_input('멘트1.png', '50%', '100%', '0px', '30px', 'left')
            if image_html1:
                st.markdown(image_html1, unsafe_allow_html=True)


            df_energy_predict = st.session_state.df_energy_predict
            df_energy_predict1 = df_energy_predict[['date','season', 'powerusage', 'optimized_powerusage','MEF_CO2']]
            df_energy_predict1['날짜']=df_energy_predict1['date'].dt.date
            df_energy_predict1['hour']=df_energy_predict1['date'].dt.hour

            st.markdown(
                f'<h2 style="font-size:24px; color:{title_color}; margin-top: 10px; margin-bottom: -10px; font-weight: bold;">1. 다음달 예측 및 최적화 결과</h2>',
                unsafe_allow_html=True)
            st.markdown(
                f"<hr style='border: 0.5px solid {hr_color}; margin-top: -10px; margin-bottom: -10px;'>",
                unsafe_allow_html=True)
            con1, con2 = st.columns([0.4,0.8])
            with con1:
                con1_1, con1_2 = st.columns([0.5, 0.5])
                with con1_1:
                    df_energy_Total=df_energy_predict1['powerusage'].sum()
                    df_energy_Total=df_energy_Total/1000
                    df_energy_Total=(df_energy_Total.round(0)).astype(int)

                    st.markdown(
                        f"""
                        <div class='centered con-margin' style='margin-top: 0px; padding: 0px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #848484;'>
                            <h2 style='font-size:30px; color:#FFFFFF; font-weight: bold;'>다음달 총 사용량
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f"""
                        <div class='centered con-margin' style='margin-top: 10px; padding:0px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #FFFFFF; max-width: 100%; margin-left: auto; margin-right: auto;'>
                            <h2 style='font-size:50px; color:black; font-weight: bold;'>
                                {df_energy_Total} MWh
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                st.markdown(
                    f"""
                    <div class='centered con-margin' style='margin-top: 10px; padding: 0px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #848484;'>
                        <h2 style='font-size:30px; color:#FFFFFF; font-weight: bold;'>다음달 절감 효과
                        </h2>
                    </div>
                    """,
                unsafe_allow_html=True
                )
                with con1_2:
                    selected_data_MEF = (df_energy_predict1['MEF_CO2'].sum()) * (-1)
                    selected_data_MEF_Total = selected_data_MEF.round(0).astype(int)


                    st.markdown(
                        f"""
                        <div class='centered con-margin' style='margin-top: 0px; padding: 0px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #848484;'>
                            <h2 style='font-size:30px; color:#FFFFFF; font-weight: bold;'>다음달 총 절감량
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f"""
                        <div class='centered con-margin' style='margin-top: 10px; padding:0px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #FFFFFF; max-width: 100%; margin-left: auto; margin-right: auto;'>
                            <h2 style='font-size:50px; color:black; font-weight: bold;'>
                                {selected_data_MEF_Total} kgCO<sub class='large-sub'>2</sub>
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    selected_data_MEF_Total1 = selected_data_MEF_Total * 1000 / 74
                    selected_data_MEF_Total1 = selected_data_MEF_Total1.round(0).astype(int)
                    selected_data_MEF_Total2=selected_data_MEF_Total/8
                    selected_data_MEF_Total2 = selected_data_MEF_Total2.round(0).astype(int)


                con2_3,con2_4 = st.columns([0.3, 0.9])
                with con2_3:
                    st.write('')
                    image_html1 = image_input('차.png','70%','60%','0px','0px','center')
                    if image_html1:
                        st.markdown(image_html1, unsafe_allow_html=True)
                with con2_4:
                    st.markdown(
                        f"""
                        <div class='centered con-margin' style='margin-top: 10px; padding: 0px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #FFFFFF; max-width: 100%; margin-left: auto; margin-right: auto;'>
                            <h2 style='font-size:30px; color:black; font-weight: bold;'>자동차 주행거리<br>
                                <span style='font-size:40px;'>{selected_data_MEF_Total1}</span>
                                <span style='font-size:30px;'>km</span>
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                con2_5,con2_6 = st.columns([0.3, 0.9])
                with con2_5:
                    st.write('')
                    image_html1 = image_input('나무.png','70%','60%','0px','0px','center')
                    if image_html1:
                        st.markdown(image_html1, unsafe_allow_html=True)
                with con2_6:
                    st.markdown(
                        f"""
                        <div class='centered con-margin' style='margin-top: 10px; padding: 0px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #FFFFFF; max-width: 100%; margin-left: auto; margin-right: auto;'>
                            <h2 style='font-size:30px; color:black; font-weight: bold;'>식재 효과<br>
                                <span style='font-size:40px;'>{selected_data_MEF_Total2}</span>
                                <span style='font-size:30px;'>그루</span>
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            with con2:
                predict_model_graph(df_energy_predict1, width=1280, height=470)

            st.markdown(
                f'<h2 style="font-size:24px; color:{title_color}; margin-top: 10px; margin-bottom: -10px; font-weight: bold;">2. 일별 최적화 및 절감량</h2>',
                unsafe_allow_html=True)
            st.markdown(
                f"<hr style='border: 0.5px solid {hr_color}; margin-top: -10px; margin-bottom: -10px;'>",
                unsafe_allow_html=True)

            # CSS 스타일 추가
            st.markdown("""
                <style>
                .stSelectbox div[data-baseweb="select"] > div {
                    background-color: white;
                }
                .stSelectbox {
                    margin-top: -20px;
                }
                </style>
                """, unsafe_allow_html=True)

            # 날짜 선택
            selected_date = st.selectbox('날짜를 선택하세요', df_energy_predict1['날짜'].unique())

            # 선택된 데이터 필터링
            selected_data = df_energy_predict1[df_energy_predict1['날짜'] == selected_date]

            if not selected_data.empty:
                st.write(f"선택된 날짜: {selected_date}")

            con1, con2, con3 = st.columns([0.4,0.4,0.4])
            with con1:
                con1_1, con1_2 = st.columns([0.5, 0.5])
                with con1_1:
                    selected_data_total=(selected_data['powerusage'].sum())
                    selected_data_total = selected_data_total.round(0).astype(int)

                    st.markdown(
                        f"""
                        <div class='centered con-margin' style='margin-top: 0px; padding: 0px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #848484;'>
                            <h2 style='font-size:30px; color:#FFFFFF; font-weight: bold;'>일별 총 사용량
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f"""
                        <div class='centered con-margin' style='margin-top: 10px; padding:0px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #FFFFFF; max-width: 100%; margin-left: auto; margin-right: auto;'>
                            <h2 style='font-size:50px; color:black; font-weight: bold;'>
                                {selected_data_total} MWh
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                with con1_2:
                    selected_data_MEF=(selected_data['MEF_CO2'].sum())* (-1)
                    selected_data_MEF_Total = selected_data_MEF.round(0).astype(int)
                    st.markdown(
                        f"""
                           <div class='centered con-margin' style='margin-top: 0px; padding: 0px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #848484;'>
                               <h2 style='font-size:30px; color:#FFFFFF; font-weight: bold;'>일별 총 절감량
                               </h2>
                           </div>
                           """,
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f"""
                           <div class='centered con-margin' style='margin-top: 10px; padding:0px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #FFFFFF; max-width: 100%; margin-left: auto; margin-right: auto;'>
                               <h2 style='font-size:50px; color:black; font-weight: bold;'>
                                   {selected_data_MEF_Total} kgCO<sub class='large-sub'>2</sub>
                               </h2>
                           </div>
                           """,
                        unsafe_allow_html=True
                    )

                    selected_data_MEF_Total1 = selected_data_MEF_Total * 1000 / 74
                    selected_data_MEF_Total1 = selected_data_MEF_Total1.round(0).astype(int)
                    selected_data_MEF_Total2=selected_data_MEF_Total/8
                    selected_data_MEF_Total2 = selected_data_MEF_Total2.round(0).astype(int)
                st.markdown(
                    f"""
                    <div class='centered con-margin' style='margin-top: 10px; padding: 0px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #848484;'>
                        <h2 style='font-size:30px; color:#FFFFFF; font-weight: bold;'>일별 절감 효과
                        </h2>
                    </div>
                    """,
                unsafe_allow_html=True
                )
                con2_3, con2_4 = st.columns([0.3, 0.9])
                with con2_3:
                    st.write('')
                    image_html1 = image_input('차.png', '70%', '60%', '0px', '0px', 'center')
                    if image_html1:
                        st.markdown(image_html1, unsafe_allow_html=True)
                with con2_4:
                    st.markdown(
                        f"""
                        <div class='centered con-margin' style='margin-top: 10px; padding: 0px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #FFFFFF; max-width: 100%; margin-left: auto; margin-right: auto;'>
                            <h2 style='font-size:30px; color:black; font-weight: bold;'>자동차 주행거리<br>
                                <span style='font-size:40px;'>{selected_data_MEF_Total1}</span>
                                <span style='font-size:30px;'>km</span>
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                con2_5, con2_6 = st.columns([0.3, 0.9])
                with con2_5:
                    st.write('')
                    image_html1 = image_input('나무.png', '70%', '60%', '0px', '0px', 'center')
                    if image_html1:
                        st.markdown(image_html1, unsafe_allow_html=True)
                with con2_6:
                    st.markdown(
                        f"""
                        <div class='centered con-margin' style='margin-top: 10px; padding: 0px; border: 0px solid #9da8ab; border-radius: 50px; text-align: center; background-color: #FFFFFF; max-width: 100%; margin-left: auto; margin-right: auto;'>
                            <h2 style='font-size:30px; color:black; font-weight: bold;'>식재 효과<br>
                                <span style='font-size:40px;'>{selected_data_MEF_Total2}</span>
                                <span style='font-size:30px;'>그루</span>
                            </h2>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    with con2:
                        create_comparison_graph1(selected_data, selected_date, width=600, height=470)
                    with con3:
                        MEF_comparison_graph(selected_data, selected_date, width=600, height=470)


            st.markdown(
                f'<h2 style="font-size:24px; color:{title_color}; margin-top: 10px; margin-bottom: -10px; font-weight: bold;">3. 최적화 결과 파일 저장</h2>',
                unsafe_allow_html=True)
            st.markdown(
                f"<hr style='border: 0.5px solid {hr_color}; margin-top: -10px; margin-bottom: -10px;'>",
                unsafe_allow_html=True)
            df_energy_predict = st.session_state.df_energy_predict

            st.markdown("<div class='reduced-margin-3'>  ↓↓↓  버튼을 누르면 아래 최적화 결과 파일을 출력할 수 있습니다.</div>", unsafe_allow_html=True)

            csv = df_energy_predict.to_csv(index=True).encode('utf-8-sig')

            # CSS와 HTML을 사용하여 버튼을 우측 정렬
            st.markdown("""
                <style>
                .download-button-container {
                    display: flex;
                    justify-content: flex-end;
                    margin-top: 0px; /* 버튼과 상단 컨텐츠 사이의 간격 조절 */
                }
                </style>
                <div class="download-button-container">
                """, unsafe_allow_html=True)

            st.markdown("""
                <div class="download-button-container">
                """, unsafe_allow_html=True)

            # 다운로드 버튼 생성
            st.download_button(
                label="CSV로 다운로드",
                data=csv,
                file_name='예측 최적화 결과.csv',
                mime='text/csv',
            )

            st.markdown("</div>", unsafe_allow_html=True)

            st.write(df_energy_predict)
        else:
            st.error("Please upload the CSV file by clicking the 'Click this!!' button.")
        st.markdown(
            f"<hr style='border: 2.0px solid {hr_color}; margin-top: -10px; margin-bottom: -10px;'>",
            unsafe_allow_html=True)

if st.session_state.selected_option == "한계배출계수 Detail":
    with st.container():
        image_html1 = image_input('효과설명3.png', '40%', '60%', '-25px', '15px', 'left')
        if image_html1:
            st.markdown(image_html1, unsafe_allow_html=True)

        # 구분선 추가
        st.markdown(
            f"<hr style='border: 2.0px solid {hr_color}; margin-top: 0px; margin-bottom: 0px;'>",
            unsafe_allow_html=True)


        # 스타일 정의
        st.markdown(
            f"""
            <style>
            .reduced-margin-3 {{
                margin-top: 0px;
                margin-bottom: -10px;
                padding-top: 0px;
                padding-bottom: 0px;
                line-height: 1.0;
                color: {text_color};
            }}            
            .centered {{
                display: flex;
                justify-content: center;
                align-items: center;
                flex-direction: column;
            }}
            .large-sub {{
                font-size: 0.6em; /* Adjust this value to change the size of the subscript */
            }}
            </style>
            """,
            unsafe_allow_html=True
        )

        if not st.session_state.energy_value_season.empty:
            image_html1 = image_input('멘트1.png', '50%', '100%', '0px', '30px', 'left')
            if image_html1:
                st.markdown(image_html1, unsafe_allow_html=True)
            con1,A, con2 = st.columns([0.5, 0.05, 0.5])
            with con1:
                st.markdown(
                    f'<h2 style="font-size:24px; color:{title_color}; margin-top: 10px; margin-bottom: -10px; font-weight: bold;">1. 한계배출계수_주중</h2>',
                    unsafe_allow_html=True)
                st.markdown(
                    f"<hr style='border: 0.5px solid {hr_color}; margin-top: -10px; margin-bottom: -10px;'>",
                    unsafe_allow_html=True)
                selected_year_weekday = st.selectbox('Select Year for 주중', ['2022', '2021', '2020'], key='weekday_year')
                selected_key_weekday = f'주중_{selected_year_weekday}'
                data_to_plot_weekday = st.session_state.mef_data[selected_key_weekday]
                MEF_graph(data_to_plot_weekday, width=900, height=400, A='주중')

            with con2:
                st.markdown(
                    f'<h2 style="font-size:24px; color:{title_color}; margin-top: 10px; margin-bottom: -10px; font-weight: bold;">2. 한계배출계수_주말</h2>',
                    unsafe_allow_html=True)
                st.markdown(
                    f"<hr style='border: 0.5px solid {hr_color}; margin-top: -10px; margin-bottom: -10px;'>",
                    unsafe_allow_html=True)
                selected_year_weekend = st.selectbox('Select Year for 주말', ['2022', '2021', '2020'], key='weekend_year')
                selected_key_weekend = f'주말_{selected_year_weekend}'
                data_to_plot_weekend = st.session_state.mef_data[selected_key_weekend]
                MEF_graph(data_to_plot_weekend, width=900, height=400, A='주말')
        else:
            st.error("Please upload the CSV file by clicking the 'Click this!!' button.")
        st.markdown(
            f"<hr style='border: 2.0px solid {hr_color}; margin-top: -10px; margin-bottom: -10px;'>",
            unsafe_allow_html=True)
