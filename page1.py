# energy_overview.py
import base64
import os

import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# 계절 판별 함수
def get_season(date):
    month = date.month
    if month in [3, 4, 5]:
        return '봄'
    elif month in [6, 7, 8]:
        return '여름'
    elif month in [9, 10, 11]:
        return '가을'
    else:
        return '겨울'

# 계절별 데이터 병합 함수
def season_graph(A):
    A['계절'] = A.index.to_series().apply(get_season)
    seasons = A.groupby('계절').sum()
    seasons = seasons.reindex(['봄', '여름', '가을', '겨울'])
    return seasons

# 데이터 입력 함수
def data_input(file_path):
    # 파일 읽기 및 날짜 인덱스 설정
    df = pd.read_csv(file_path)
    df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    df = df.sort_values(by='datetime', ascending=True)
    df.drop(['year', 'month', 'day', 'hour'], axis=1, inplace=True)
    return df

def MEF_graph(data, width, height,A):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=data['Hour'], y=data['봄'], mode='lines+markers', name='봄',
                             marker=dict(symbol='x', color='red', size=7), line=dict(color='red', width=1)))
    fig.add_trace(
        go.Scatter(x=data['Hour'], y=data['여름'], mode='lines+markers', name='여름',
                   marker=dict(symbol='circle', color='blue', size=7), line=dict(color='blue', width=1)))
    fig.add_trace(
        go.Scatter(x=data['Hour'], y=data['가을'], mode='lines+markers', name='가을',
                   marker=dict(symbol='diamond', color='green', size=7), line=dict(color='green', width=1)))
    fig.add_trace(
        go.Scatter(x=data['Hour'], y=data['겨울'], mode='lines+markers', name='겨울',
                   marker=dict(symbol='triangle-up', color='orange', size=7),
                   line=dict(color='orange', width=1)))

    fig.update_layout(
        plot_bgcolor='rgba(255, 255, 255, 1)',  # 배경색을 흰색으로 설정
        paper_bgcolor='rgba(255, 255, 255, 1)',  # 종이 배경색을 흰색으로 설정
        legend=dict(font=dict(color='#9da8ab')),
        xaxis=dict(
            tickfont=dict(color='#9da8ab'),
            title=dict(text='Hour of the Day', font=dict(color='#9da8ab'))
        ),
        yaxis=dict(
            tickfont=dict(color='#9da8ab'),
            title=dict(text='한계배출계수(kgCO2/kWh)', font=dict(color='#9da8ab')),
            range=[0, 1.0]  # Set y-axis range here
        ),
        autosize=True,  # 그래프 자동 크기 조절
        width=width,  # 그래프 너비 지정
        height=height,  # 그래프 높이 지정
        title=dict(text=f'{A} 한계배출계수 그래프', font=dict(color='#9da8ab'), x=0.5, xanchor='center')
    )

    # 그래프를 HTML로 변환
    html_str = fig.to_html(full_html=False)

    # 스타일과 함께 HTML을 Streamlit에 표시
    st.components.v1.html(f"""
    <div style="display: flex; justify-content: center;">
        <div style="border: 2px solid black; border-radius: 10px; padding: 10px; width: {width}px;">
            {html_str}
        </div>
    </div>
    """, height=height + 40, width=width + 40)

def image_input(A, width, height, margin_top, margin_bottom,array):
    current_dir = os.path.dirname(__file__)
    image_path = os.path.join(current_dir, 'image', A)

    if os.path.exists(image_path):
        with open(image_path, "rb") as image_file:
            encoded_image = base64.b64encode(image_file.read()).decode()

        return f"""
        <div style="display: flex; justify-content: {array}; align-items: center; height: 100%; width: 100%; margin-top: {margin_top}; margin-bottom: {margin_bottom};">
            <img src="data:image/png;base64,{encoded_image}" alt="대표 이미지" style="max-width: {width}; height: {height};">
        </div>
        """

def season_bar(data, width, height):
    fig = go.Figure()
    fig.add_trace(go.Bar(x=data.index, y=data.values, marker=dict(color=['red', 'blue', 'green', 'orange']),
                         text=data.values, textfont=dict(color='white'), textposition='auto', width=[0.5] * len(data)))
    fig.update_layout(
        plot_bgcolor='rgba(255, 255, 255, 1)',  # 배경색을 흰색으로 설정
        paper_bgcolor='rgba(255, 255, 255, 1)',  # 종이 배경색을 흰색으로 설정
        legend=dict(y=-0.2, x=0.5, xanchor='center', orientation='h', font=dict(color='#9da8ab')),
        xaxis=dict(
            tickfont=dict(color='#9da8ab'),
            title=dict(text='Season', font=dict(color='#9da8ab'))
        ),
        yaxis=dict(
            tickfont=dict(color='#9da8ab'),
            title=dict(text='Total Energy Usage', font=dict(color='#9da8ab'))
        ),
        autosize=True,  # 그래프 자동 크기 조절
        width=width,  # 그래프 너비 지정
        height=height,  # 그래프 높이 지정
        title=dict(text='Energy Usage by Season', font=dict(color='#9da8ab'), x=0.5, xanchor='center')
    )

    # 그래프를 HTML로 변환
    html_str = fig.to_html(full_html=False)

    # 스타일과 함께 HTML을 Streamlit에 표시
    st.components.v1.html(f"""
    <div style="display: flex; justify-content: center;">
        <div style="border: 2px solid black; border-radius: 10px; padding: 10px; width: {width}px;">
            {html_str}
        </div>
    </div>
    """, height=height + 40, width=width + 40)


def season_MEF_bar(data, width, height):
    fig = go.Figure()
    data['MEF_CO2'] = data['MEF_CO2'] / 1000
    fig.add_trace(go.Bar(x=data['season'], y=data['MEF_CO2'], marker=dict(color=['red', 'blue', 'green', 'orange']),
                         text=data['MEF_CO2'], textfont=dict(color='white'), textposition='auto', width=[0.5] * len(data)))
    fig.update_layout(
        plot_bgcolor='rgba(255, 255, 255, 1)',  # 배경색을 흰색으로 설정
        paper_bgcolor='rgba(255, 255, 255, 1)',  # 종이 배경색을 흰색으로 설정
        legend=dict(y=-0.2, x=0.5, xanchor='center', orientation='h', font=dict(color='#9da8ab')),
        xaxis=dict(
            tickfont=dict(color='#9da8ab'),
            title=dict(text='Season', font=dict(color='#9da8ab'))
        ),
        yaxis=dict(
            tickfont=dict(color='#9da8ab'),
            title=dict(text='CO<sub>2</sub> Reduction (tCO<sub>2</sub>)', font=dict(color='#9da8ab'))
        ),
        autosize=True,  # 그래프 자동 크기 조절
        title=dict(text='CO2 Reduction by Season', font=dict(color='#9da8ab'),
                   x=0.5, xanchor='center')
    )

    # Streamlit에 그래프 표시
    st.plotly_chart(fig, use_container_width=True)
