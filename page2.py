import pandas as pd
from prophet import Prophet
import streamlit as st
import plotly.graph_objects as go

def predict_model(file):
    # 데이터 로드
    data = pd.read_csv(file)
    data['ds'] = pd.to_datetime(data[['year', 'month', 'day', 'hour']])
    data['y'] = data['powerusage']
    data = data.sort_values(by='ds')
    # 연간, 주간, 일간 계절성 / 커스텀 계절성 추가
    model = Prophet(yearly_seasonality=True, weekly_seasonality=True, daily_seasonality=True)
    model.add_seasonality(name='monthly', period=30.5, fourier_order=5)
    # 모델 학습
    model.fit(data[['ds', 'y']])
    future_dates = pd.date_range(start='2021-01-01', end='2021-01-31 23:00:00', freq='H')
    future = pd.DataFrame({'ds': future_dates})
    # 미래 데이터 예측 및
    forecast = model.predict(future)
    # print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())
    # forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].to_csv(
    #     r'C:\Users\user\Desktop\EMS 데이터\lstm_data\forecast_results_array_3.csv', index=False)
    # fig1=model.plot(forecast)
    # fig2=model.plot_components(forecast)
    forecast=forecast[['ds', 'yhat']]
    return forecast


def predict_model_graph(df, width, height):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df['date'], y=df['powerusage'], mode='lines', line=dict(color='blue'), name='기존 사용량'))
    fig.add_trace(
        go.Scatter(x=df['date'], y=df['optimized_powerusage'], mode='lines', line=dict(color='red'), name='최적화 사용량'))

    fig.update_layout(
        plot_bgcolor='rgba(255, 255, 255, 1)',  # 배경색을 흰색으로 설정
        paper_bgcolor='rgba(255, 255, 255, 1)',  # 종이 배경색을 흰색으로 설정
        legend=dict(y=-0.2, x=0.5, xanchor='center', orientation='h', font=dict(color='#9da8ab')),
        xaxis=dict(
            tickfont=dict(color='#9da8ab'),
            title=dict(text='Hour of the Day', font=dict(color='#9da8ab'))
        ),
        yaxis=dict(
            tickfont=dict(color='#9da8ab'),
            title=dict(text='Average Value', font=dict(color='#9da8ab')),
            range=[0, max(df[['powerusage', 'optimized_powerusage']].max()) + 10]
        ),
        title=dict(
            text=f"최적화 그래프 ({df['date'].dt.year.unique()[0]})",
            font=dict(color='#9da8ab', size=20),
            y=0.9,
            x=0.5,
            xanchor='center'
        ),
        autosize=True,  # 그래프 자동 크기 조절
        width=width,  # 그래프 너비 지정
        height=height  # 그래프 높이 지정
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

# def predict_model_graph(df, width, height):
#     fig = go.Figure()
#     fig.add_trace(go.Scatter(x=df['date'], y=df['powerusage'], mode='lines', line=dict(color='blue'), name='기존 사용량'))
#     fig.add_trace(
#         go.Scatter(x=df['date'], y=df['optimized_powerusage'], mode='lines', line=dict(color='red'), name='최적화 사용량'))
#
#     fig.update_layout(
#         plot_bgcolor='rgba(255, 255, 255, 1)',  # 배경색을 흰색으로 설정
#         paper_bgcolor='rgba(255, 255, 255, 1)',  # 종이 배경색을 흰색으로 설정
#         legend=dict(y=-0.3, x=0.5, xanchor='center', orientation='h', font=dict(color='#9da8ab')),
#         xaxis=dict(
#             tickfont=dict(color='#9da8ab'),
#             title=dict(text='Hour of the Day', font=dict(color='#9da8ab'))
#         ),
#         yaxis=dict(
#             tickfont=dict(color='#9da8ab'),
#             title=dict(text='Average Value', font=dict(color='#9da8ab')),
#             range=[0, max(df[['powerusage', 'optimized_powerusage']].max()) + 10]
#         ),
#         width=width,  # 그래프 너비 지정
#         height=height  # 그래프 높이 지정
#     )
#
#     # 그래프를 HTML로 변환
#     html_str = fig.to_html(full_html=False)
#
#     # 스타일과 함께 HTML을 Streamlit에 표시
#     st.components.v1.html(f"""
#     <div style="display: flex; justify-content: center; width: 100%;">
#         <div style="border: 2px solid black; border-radius: 10px; padding: 10px; width: 100%; max-width: {width}px;">
#             {html_str}
#         </div>
#     </div>
#     """, height=height + 40, width=width + 40)
