#!/usr/bin/env python3

import requests

def fetch_prometheus_data(prometheus_url, metric_name):
    '''
    从Prometheus服务器获取指定指标的数据。
    
    参数:
    - prometheus_url (str): Prometheus服务器的URL，例如 'http://localhost:9090'.
    - metric_name (str): 要查询的指标名称。
    
    返回:
    - dict: 查询结果，包含时间序列数据。如果请求失败或无数据，返回None。
    
    注意:
    此函数使用Prometheus的API直接查询数据，要求Prometheus服务器支持HTTP API访问。
    '''
    # Prometheus的API端点用于查询数据
    query_endpoint = f'{prometheus_url}/api/v1/query'
    
    # 构建查询参数
    params = {
        'query': metric_name,
        'time': None,  # 可以指定时间，留空则默认为当前时间
    }
    
    try:
        # 发起GET请求到Prometheus查询API
        response = requests.get(query_endpoint, params=params)
        
        # 确保请求成功
        if response.status_code == 200:
            data = response.json()
            
            # 检查查询是否有结果
            if data['status'] == 'success' and data['data']['result']:
                return data['data']['result']
            else:
                print('没有找到对应的数据。')
                return None
        else:
            print(f'请求Prometheus时发生错误，状态码：{response.status_code}')
            return None
    except requests.RequestException as e:
        print(f'请求过程中发生错误：{e}')
        return None

# 使用示例
if __name__ == '__main__':
    prometheus_server = 'http://10.8.0.2:9090'  # 替换为实际的Prometheus服务器地址
    metric_to_query = 'temp_22{job="mijia"}'  # 示例指标名，根据实际情况替换
    result = fetch_prometheus_data(prometheus_server, metric_to_query)
    
    if result:
        print('获取到的数据：', result)
    else:
        print('未能成功获取数据。')