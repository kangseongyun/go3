import pandas as pd
import numpy as np
from scipy.optimize import minimize
from page3_sub import spread, data_input1,get_season

def optimize_data(mef_path_주중, mef_path_주말, e_path):
    # if 'ds' in e_path.columns and 'yhat' in e_path.columns:
    #     e_path = e_path.rename(columns={'ds': 'date', 'yhat': 'powerusage'})

    # 데이터 불러오기
    df_mef_주중 = pd.read_csv(mef_path_주중, index_col='Hour')
    df_mef_주말 = pd.read_csv(mef_path_주말, index_col='Hour')

    # 주중과 주말에 따라 다른 MEF 값을 적용
    def get_mef_value(row):
        if row['weekday_status'] == 'O':  # 주중
            return df_mef_주중.loc[row['hour'], row['season']]
        else:  # 주말
            return df_mef_주말.loc[row['hour'], row['season']]
    e_path['MEF'] = e_path.apply(lambda row: get_mef_value(row), axis=1)

    # 계절 및 시간대별 cut-off 값 계산
    cutoff_values = spread(e_path)

    # df_energy에 min_cutoff와 max_cutoff 열 추가
    df_energy = e_path.merge(cutoff_values, on=['season', 'weekday_status', 'hour'], how='left')

    def calculate_seasonal_hourly_changes(df_energy):
        df_energy['season'] = df_energy['month'].apply(get_season)
        # 주중과 주말을 구분하여 변화율의 평균 계산
        주중 = df_energy[df_energy['weekday_status'] == 'O'].copy()
        주말 = df_energy[df_energy['weekday_status'] == 'X'].copy()
        def cal(df):
            # 전날 같은 시간의 powerusage를 계산
            df['previous_day_powerusage'] = df['powerusage'].shift(24)

            # 변화율 계산
            df['change_rate'] = (df['powerusage'] / df['previous_day_powerusage']) * 100

            # NaN 값 제거 (변화율 계산 불가능한 첫 24시간 제거)
            df.dropna(subset=['change_rate'], inplace=True)


            # 100보다 큰 경우와 작은 경우로 구분
            df['change_rate_gt_100'] = df['change_rate'] >= 100
            return df
        주중=cal(주중)
        주말=cal(주말)



        # 주중 - 100보다 큰 경우와 작은 경우로 구분하여 평균 계산
        주중_100이상 = 주중[주중['change_rate_gt_100']].groupby(['season', 'hour'])['change_rate'].mean().reset_index()
        주중_100미만 = 주중[~주중['change_rate_gt_100']].groupby(['season', 'hour'])['change_rate'].mean().reset_index()

        # 주말 - 100보다 큰 경우와 작은 경우로 구분하여 평균 계산
        주말_100이상 = 주말[주말['change_rate_gt_100']].groupby(['season', 'hour'])['change_rate'].mean().reset_index()
        주말_100미만 = 주말[~주말['change_rate_gt_100']].groupby(['season', 'hour'])['change_rate'].mean().reset_index()

        # 열 이름 변경
        주중_100이상.rename(columns={'change_rate': '변화율_100이상_주중'}, inplace=True)
        주중_100미만.rename(columns={'change_rate': '변화율_100미만_주중'}, inplace=True)
        주말_100이상.rename(columns={'change_rate': '변화율_100이상_주말'}, inplace=True)
        주말_100미만.rename(columns={'change_rate': '변화율_100미만_주말'}, inplace=True)

        # 결과 출력
        return 주중_100이상, 주중_100미만, 주말_100이상, 주말_100미만

    # 함수 호출
    주중_100이상, 주중_100미만, 주말_100이상, 주말_100미만 = calculate_seasonal_hourly_changes(df_energy)
    with pd.ExcelWriter('seasonal_hourly_changes.xlsx') as writer:
        주중_100이상.to_excel(writer, sheet_name='주중_100이상', index=False)
        주중_100미만.to_excel(writer, sheet_name='주중_100미만', index=False)
        주말_100이상.to_excel(writer, sheet_name='주말_100이상', index=False)
        주말_100미만.to_excel(writer, sheet_name='주말_100미만', index=False)
    # '변화율제약' 열 추가
    df_energy = df_energy.merge(주중_100이상, on=['season', 'hour'], how='left')
    df_energy = df_energy.merge(주중_100미만, on=['season', 'hour'], how='left')
    df_energy = df_energy.merge(주말_100이상, on=['season', 'hour'], how='left')
    df_energy = df_energy.merge(주말_100미만, on=['season', 'hour'], how='left')

    if 'O' in df_energy['weekday_status'].values:  # 주중인 경우
        df_energy['최대제한'] = df_energy['powerusage'] * df_energy['변화율_100이상_주중'] / 100
        df_energy['최소제한'] = df_energy['powerusage'] * df_energy['변화율_100미만_주중'] / 100
    else:  # 주말인 경우
        df_energy['최대제한'] = df_energy['powerusage'] * df_energy['변화율_100이상_주말'] / 100
        df_energy['최소제한'] = df_energy['powerusage'] * df_energy['변화율_100미만_주말'] / 100

    grouped_data = df_energy.groupby('날짜')

    optimization_results = []
    prev_day_optimized = None  # 전날 23시 최적화 값을 저장할 변수
    prev_day_original = None  # 전날 23시 원래 값을 저장할 변수

    for name, group in grouped_data:
        min_max_day = group['powerusage'].min()
        valid_indices_group = np.where(group['powerusage'] >= min_max_day)[0]

        if len(valid_indices_group) > 0:
            co2_emission_factor_group = group['MEF'].values
            initial_power_usage_group = group['powerusage'].values
            x0_group = initial_power_usage_group[valid_indices_group].copy()

            def objective_group(x):
                emissions = co2_emission_factor_group[valid_indices_group] * (x - initial_power_usage_group[valid_indices_group])
                return np.sum(emissions)

            def resist1(x):
                return np.sum(x) - np.sum(initial_power_usage_group[valid_indices_group])

            def resist1_1(x):
                original_total_usage = np.sum(initial_power_usage_group[valid_indices_group])
                optimized_total_usage = np.sum(x)
                # 10% 증가를 허용하는 제약 조건 설정
                return optimized_total_usage - 0.9 * original_total_usage

            def resist2(x):
                return x - min_max_day


            def resist3(x):
                initial_rates_group = np.append(0, np.diff(initial_power_usage_group[valid_indices_group]) / (
                    initial_power_usage_group[valid_indices_group][:-1]))
                new_rates_group = np.append(0, np.diff(x) / (x[:-1]))
                rate_change_diff_group = (new_rates_group - initial_rates_group) * 100
                return np.concatenate([10 - rate_change_diff_group, rate_change_diff_group + 10])

            # 계절 및 시간대별 조절 범위 제약 추가
            def resist4(x):
                min_cutoff = group['min_cutoff'].values
                max_cutoff = group['max_cutoff'].values
                return np.concatenate([x - min_cutoff, max_cutoff - x])

            def resist6(x):
                # 최대제한과 최소제한 제약조건
                max_limit = group['최대제한'].values
                min_limit = group['최소제한'].values
                return np.concatenate([x - min_limit, max_limit - x])

            def resist6_1(x):
                # 최대제한과 최소제한 제약조건을 0시에 대해서만 적용
                max_limit = group['최대제한'].values
                min_limit = group['최소제한'].values
                return np.array([x[0] - min_limit[0], max_limit[0] - x[0]])

            def resist6_2(x):
                # 최대제한과 최소제한 제약조건을 0시에 대해서만 적용
                max_limit = group['최대제한'].values
                min_limit = group['최소제한'].values
                return np.array([x[23] - min_limit[23], max_limit[23] - x[23]])



            constraints_group = [
                {'type': 'eq', 'fun': resist1},
                # {'type': 'eq', 'fun': resist1_1},
                {'type': 'ineq', 'fun': resist2},
                {'type': 'ineq', 'fun': resist3},
                {'type': 'ineq', 'fun': resist4},
                # {'type': 'ineq', 'fun': resist5},
                # {'type': 'ineq', 'fun': resist6},
                {'type': 'ineq', 'fun': resist6_1},
                {'type': 'ineq', 'fun': resist6_2},
                # {'type': 'ineq', 'fun': resist7},
            ]

            result_group = minimize(objective_group, x0_group, constraints=constraints_group, method='SLSQP', options={'disp': True, 'maxiter': 300})

            if result_group.success:
                optimized_power_usage_group = initial_power_usage_group.copy()
                optimized_power_usage_group[valid_indices_group] = result_group.x
                df_energy.loc[group.index, 'optimized_powerusage'] = optimized_power_usage_group
                prev_day_optimized = optimized_power_usage_group  # 현재 최적화 결과를 저장
                prev_day_original = initial_power_usage_group  # 현재 원래 값을 저장
                optimization_results.append((name, result_group.success))
            else:
                optimization_results.append((name, result_group.success, result_group.message))
        else:
            optimization_results.append((name, False, "No valid indices in this group"))

    df_energy['MEF_CO2'] = (df_energy['optimized_powerusage'] - df_energy['powerusage']) * df_energy['MEF']


    # 시간대별로 그룹화하여 평균 전력 사용량 계산
    # grouped_total = df_energy.groupby(df_energy['시간']).mean(numeric_only=True)
    # current_dir = os.path.dirname(__file__)
    # data_path = os.path.join(current_dir, 'image', '최적화결과.csv')
    #
    # df_energy.to_csv(data_path, encoding='cp949')
    return df_energy

