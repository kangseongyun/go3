import pandas as pd
import plotly.graph_objects as go
import streamlit as st

def spread(A):
    def remove_outliers_quantile(df, column):
        grouped = df.groupby('hour')
        def filter_group(group):
            return group[(group[column] > group[column].quantile(0)) & (group[column] < group[column].quantile(1.0))]
        result = grouped.apply(filter_group).reset_index(drop=True)
        quantiles = grouped[column].quantile([0, 1.0]).unstack()
        return result, quantiles

    # 계절과 주중/주말 조합 별로 데이터 필터링 및 cut-off 값 계산
    seasons = ['봄', '여름', '가을', '겨울']
    weekday_statuses = ['O', 'X']  # 'O'는 주중, 'X'는 주말

    # 결과를 저장할 리스트
    combined_cutoff_values = []

    for season in seasons:
        for status in weekday_statuses:
            # 특정 계절과 주중/주말 조합에 대한 데이터 필터링
            subset = A[(A['season'] == season) & (A['weekday_status'] == status)]
            # 아웃라이어 제거 및 cut-off 값 계산
            filtered_data, quantiles = remove_outliers_quantile(subset, 'powerusage')
            # 결과 저장
            for hour in quantiles.index:
                combined_cutoff_values.append({
                    'season': season,  # Ensure correct column naming
                    'weekday_status': status,
                    'hour': hour,
                    'min_cutoff': quantiles.loc[hour, 0.0],
                    'max_cutoff': quantiles.loc[hour, 1.0]
                })

    # 결과를 DataFrame으로 변환
    combined_df = pd.DataFrame(combined_cutoff_values)
    combined_df.to_csv(r"C:\Users\user\Desktop\종설\test.csv", index=False)  # Ensure index is not saved

    return combined_df


def get_season(month):
    if month in [3, 4, 5]:
        return '봄'
    elif month in [6, 7, 8]:
        return '여름'
    elif month in [9, 10, 11]:
        return '가을'
    else:
        return '겨울'
def data_input1(csv_file):
    # 파일 읽기 및 날짜 인덱스 설정
    df = pd.read_csv(csv_file)
    df['date'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    df = df.sort_values(by='date', ascending=True)
    df['date'] = pd.to_datetime(df['date'])
    df['weekday'] = df['date'].dt.dayofweek
    df['day_name'] = df['date'].dt.day_name()
    df['weekday_status'] = df['weekday'].apply(lambda x: 'O' if x < 5 else 'X')
    df['hour'] = df['date'].dt.hour
    df['month'] = df['date'].dt.month
    df['season'] = df['month'].apply(get_season)
    df['날짜'] = df['date'].dt.date
    return df

def data_input2(csv_file):
    # 파일 읽기 및 날짜 인덱스 설정
    # df['date'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    df = csv_file.rename(columns={'ds':'date','yhat':'powerusage'})
    df = df.sort_values(by='date', ascending=True)
    df['date'] = pd.to_datetime(df['date'])
    df['weekday'] = df['date'].dt.dayofweek
    df['day_name'] = df['date'].dt.day_name()
    df['weekday_status'] = df['weekday'].apply(lambda x: 'O' if x < 5 else 'X')
    df['hour'] = df['date'].dt.hour
    df['month'] = df['date'].dt.month
    df['season'] = df['month'].apply(get_season)
    df['날짜'] = df['date'].dt.date
    return df

# def create_comparison_graph(df_energy, selected_date):
#     fig = go.Figure()
#     df_selected = df_energy[df_energy['날짜'] == selected_date]
#     hours = df_selected['hour']
#     original_usage = df_selected['powerusage']
#     optimized_usage = df_selected['optimized_powerusage']
#     # 기존 전력 사용량 그래프
#     fig.add_trace(go.Scatter(
#         x=hours, y=original_usage, mode='lines', name='기존 전력 사용량', line=dict(color='blue')
#     ))
#
#     # 최적화된 전력 사용량 그래프
#     fig.add_trace(go.Scatter(
#         x=hours, y=optimized_usage, mode='lines', name='최적화된 전력 사용량', line=dict(color='red')
#     ))
#
#     fig.update_layout(
#         plot_bgcolor='rgba(255, 255, 255, 1)',  # 배경색을 흰색으로 설정
#         paper_bgcolor='rgba(255, 255, 255, 1)',  # 종이 배경색을 흰색으로 설정
#         title=dict(
#             text=f"최적화 그래프 ({selected_date})",
#             font=dict(color='#9da8ab', size=20),
#             x=0.5,
#             xanchor='center'
#         ),
#         xaxis_title=dict(text="시간", font=dict(color='#9da8ab')),
#         yaxis_title=dict(text="전력 사용량", font=dict(color='#9da8ab')),
#         legend=dict(y=-0.2, x=0.5, xanchor='center', orientation='h', font=dict(color='#9da8ab')),
#         xaxis=dict(showline=True, zeroline=False, color='#9da8ab', tickfont=dict(color='#9da8ab')),
#         yaxis=dict(showline=True, zeroline=False, color='#9da8ab', tickfont=dict(color='#9da8ab'),
#         range=[0, max(df_selected[['powerusage', 'optimized_powerusage']].max()) + 10]),
#         autosize=True
#     )
#     return st.plotly_chart(fig, use_container_width=True)


# def create_comparison_graph(df_energy, selected_date, width, height):
#     fig = go.Figure()
#     df_selected = df_energy[df_energy['날짜'] == selected_date]
#     hours = df_selected['hour']
#     original_usage = df_selected['powerusage']
#     optimized_usage = df_selected['optimized_powerusage']
#     # 기존 전력 사용량 그래프
#     fig.add_trace(go.Scatter(
#         x=hours, y=original_usage, mode='lines', name='기존 전력 사용량', line=dict(color='blue')
#     ))
#
#     # 최적화된 전력 사용량 그래프
#     fig.add_trace(go.Scatter(
#         x=hours, y=optimized_usage, mode='lines', name='최적화된 전력 사용량', line=dict(color='red')
#     ))
#
#     fig.update_layout(
#         plot_bgcolor='rgba(255, 255, 255, 1)',  # 배경색을 흰색으로 설정
#         paper_bgcolor='rgba(255, 255, 255, 1)',  # 종이 배경색을 흰색으로 설정
#         title=dict(
#             text=f"최적화 그래프 ({selected_date})",
#             font=dict(color='#9da8ab', size=20),
#             x=0.5,
#             xanchor='center'
#         ),
#         xaxis_title=dict(text="시간", font=dict(color='#9da8ab')),
#         yaxis_title=dict(text="전력 사용량", font=dict(color='#9da8ab')),
#         legend=dict(y=-0.3, x=0.5, xanchor='center', orientation='h', font=dict(color='#9da8ab')),
#         xaxis=dict(showline=True, zeroline=False, color='#9da8ab', tickfont=dict(color='#9da8ab')),
#         yaxis=dict(showline=True, zeroline=False, color='#9da8ab', tickfont=dict(color='#9da8ab'),
#         range=[0, max(df_selected[['powerusage', 'optimized_powerusage']].max()) + 10]),
#         width=width,  # 그래프 너비 지정
#         height=height  # 그래프 높이 지정
#     )
#     # 그래프를 HTML로 변환
#     html_str = fig.to_html(full_html=False)
#
#     # 스타일과 함께 HTML을 Streamlit에 표시
#     st.components.v1.html(f"""
#     <div style="display: flex; justify-content: center;">
#         <div style="border: 2px solid black; border-radius: 10px; padding: 10px; width: {width}px;">
#             {html_str}
#         </div>
#     </div>
#     """, height=height+40, width=width+40)




def create_comparison_graph(df_energy, selected_date):
    fig = go.Figure()
    df_selected = df_energy[df_energy['날짜'] == selected_date]
    hours = df_selected['hour']
    original_usage = df_selected['powerusage']
    optimized_usage = df_selected['optimized_powerusage']

    # 기존 전력 사용량 그래프
    fig.add_trace(go.Scatter(
        x=hours, y=original_usage, mode='lines', name='기존 전력 사용량', line=dict(color='blue')
    ))

    # 최적화된 전력 사용량 그래프
    fig.add_trace(go.Scatter(
        x=hours, y=optimized_usage, mode='lines', name='최적화된 전력 사용량', line=dict(color='red')
    ))

    fig.update_layout(
        plot_bgcolor='rgba(255, 255, 255, 1)',  # 배경색을 흰색으로 설정
        paper_bgcolor='rgba(255, 255, 255, 1)',  # 종이 배경색을 흰색으로 설정
        title=dict(
            text=f"최적화 그래프 ({selected_date})",
            font=dict(color='#9da8ab', size=20),
            x=0.5,
            xanchor='center'
        ),
        xaxis_title=dict(text="시간", font=dict(color='#9da8ab')),
        yaxis_title=dict(text="전력사용량", font=dict(color='#9da8ab')),
        legend=dict(y=0.1, x=0.5, xanchor='center', orientation='h', font=dict(color='#9da8ab')),
        xaxis=dict(showline=True, zeroline=False, color='#9da8ab', tickfont=dict(color='#9da8ab')),
        yaxis=dict(showline=True, zeroline=False, color='#9da8ab', tickfont=dict(color='#9da8ab'),
                   range=[0, max(df_selected[['powerusage', 'optimized_powerusage']].max()) + 10]),
        autosize=True,  # 그래프 자동 크기 조절
        height=800  # 그래프의 높이를 줄임
    )

    # 그래프를 HTML로 변환
    html_str = fig.to_html(full_html=False)

    # 스타일과 함께 HTML을 Streamlit에 표시
    st.components.v1.html(f"""
        <div style="display: flex; justify-content: center; align-items: center; height: 100%;">
            <div style="border: 3px solid black; border-radius: 10px; width: 100%; max-width: 1400px;">
                {html_str}
            </div>
        </div>
        """, height=850)  # 컨테이너의 높이를 맞춤


def create_comparison_graph1(df_energy, selected_date, width, height):
    fig = go.Figure()
    df_selected = df_energy[df_energy['날짜'] == selected_date]
    hours = df_selected['hour']
    original_usage = df_selected['powerusage']
    optimized_usage = df_selected['optimized_powerusage']

    # 기존 전력 사용량 그래프
    fig.add_trace(go.Scatter(
        x=hours, y=original_usage, mode='lines', name='기존 전력 사용량', line=dict(color='blue')
    ))

    # 최적화된 전력 사용량 그래프
    fig.add_trace(go.Scatter(
        x=hours, y=optimized_usage, mode='lines', name='최적화된 전력 사용량', line=dict(color='red')
    ))

    fig.update_layout(
        plot_bgcolor='rgba(255, 255, 255, 1)',  # 배경색을 흰색으로 설정
        paper_bgcolor='rgba(255, 255, 255, 1)',  # 종이 배경색을 흰색으로 설정
        title=dict(
            text=f"최적화 그래프 ({selected_date})",
            font=dict(color='#9da8ab', size=20),
            x=0.5,
            xanchor='center'
        ),
        xaxis_title=dict(text="시간", font=dict(color='#9da8ab')),
        yaxis_title=dict(text="전력사용량", font=dict(color='#9da8ab')),
        legend=dict(y=-0.2, x=0.5, xanchor='center', orientation='h', font=dict(color='#9da8ab')),
        xaxis=dict(showline=True, zeroline=False, color='#9da8ab', tickfont=dict(color='#9da8ab')),
        yaxis=dict(showline=True, zeroline=False, color='#9da8ab', tickfont=dict(color='#9da8ab'),
                   range=[0, max(df_selected[['powerusage', 'optimized_powerusage']].max()) + 10]),
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
    """, height=height+40, width=width+40)



def MEF_comparison_graph(df_energy, selected_date, width, height):
    fig = go.Figure()
    df_selected = df_energy[df_energy['날짜'] == selected_date]
    hours = df_selected['hour']
    optimized_usage = df_selected['MEF_CO2']

    # 최적화된 전력 사용량 그래프 (바 그래프)
    fig.add_trace(go.Bar(
        x=hours, y=optimized_usage, name='시간대별 CO<sub>2</sub> 감축량', marker=dict(color='red')
    ))

    fig.update_layout(
        plot_bgcolor='rgba(255, 255, 255, 1)',  # 배경색을 흰색으로 설정
        paper_bgcolor='rgba(255, 255, 255, 1)',  # 종이 배경색을 흰색으로 설정
        title=dict(
            text=f"시간대별 CO<sub>2</sub> 감축 그래프 ({selected_date})",
            font=dict(color='#9da8ab', size=20),
            x=0.5,
            xanchor='center'
        ),
        xaxis_title=dict(text="시간", font=dict(color='#9da8ab')),
        yaxis_title=dict(text="kgCO<sub>2</sub>", font=dict(color='#9da8ab')),
        xaxis=dict(showline=True, zeroline=False, color='#9da8ab', tickfont=dict(color='#9da8ab')),
        yaxis=dict(showline=True, zeroline=False, color='#9da8ab', tickfont=dict(color='#9da8ab')),
        legend=dict(y=-0.2, x=0.5, xanchor='center', orientation='h', font=dict(color='#9da8ab')),
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
    """, height=height+40, width=width+40)
