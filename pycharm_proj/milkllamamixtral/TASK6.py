
def predict(text, max_predictions=10, min_confidence=0.1, max_length=256,
num_threads=1, cache=True, **kwargs):
    if isinstance(text, (list, tuple)):
        requests = [{'text': t} for t in text]
    else:
        requests = [{'text': text}]
        return send_requests('POST', '/predict', requests, max_predictions,
    min_confidence, max_length, num_threads, cache, **kwargs)

def summarize_tasks(task_ids, max_predictions=10, min_confidence=0.1,
max_length=256, num_threads=1, cache=True, **kwargs):
    requests = [{'task_id': t} for t in task_ids]
    return send_requests('POST', '/summarize_tasks', requests,
max_predictions, min_confidence, max_length, num_threads, cache, **kwargs)

def predict(text, max_predictions=10, min_confidence=0.1, max_length=256,
num_threads=1, cache=True, **kwargs):
    requests = [{'text': text}]
    return send_requests('POST', '/predict', requests, max_predictions,
min_confidence, max_length, num_threads, cache, **kwargs)

def summarize_tasks(task_ids, max_predictions=10, min_confidence=0.1,
max_length=256, num_threads=1, cache=True, **kwargs):
    requests = [{'task_id': t} for t in task_ids]
    return send_requests('POST', '/summarize_tasks', requests,
max_predictions, min_confidence, max_length, num_threads, cache, **kwargs)

def predict(text, max_predictions=10, min_confidence=0.1, max_length=256,
num_threads=1, cache=True, **kwargs):
    requests = [{'text': text}]
    return send_requests('POST', '/predict', requests, max_predictions,
min_confidence, max_length, num_threads, cache, **kwargs)

def summarize_tasks(task_ids, max_predictions=10, min_confidence=0.1,
max_length=256, num_threads=1, cache=True, **kwargs):
    requests = [{'task_id': t} for t in task_ids]
    return send_requests('POST', '/summarize_tasks', requests,
max_predictions, min_confidence, max_length, num_threads, cache, **kwargs)

def predict(text, max_predictions=10, min_confidence=0.1, max_length=256,
num_threads=1, cache=True, **kwargs):
    requests = [{'text': text}]
    return send_requests('POST', '/predict', requests, max_predictions,
min_confidence, max_length, num_threads, cache, **kwargs)

def summarize_tasks(task_ids, max_predictions=10, min_confidence=0.1,
max_length=256, num_threads=1, cache=True, **kwargs):
    requests = [{'task_id': t} for t in task_ids]
    return send_requests('POST', '/summarize_tasks', requests,
max_predictions, min_confidence, max_length, num_threads, cache, **kwargs)

def predict(text, max_predictions=10, min_confidence=0.1, max_length=256,
num_threads=1, cache=True, **kwargs):
    requests = [{'text': text}]
    return send_requests('POST', '/predict', requests, max_predictions,
min_confidence, max_length, num_threads, cache, **kwargs)

def summarize_tasks(task_ids, max_predictions=10, min_confidence=0.1,
max_length=256, num_threads=1, cache=True, **kwargs):
    requests = [{'task_id': t} for t in task_ids]
    return send_requests('POST', '/summarize_tasks', requests,
max_predictions, min_confidence, max_length, num_threads, cache, **kwargs)

def predict(text, max_predictions=10, min_confidence=0.1, max_length=256,
num_threads=1, cache=True, **kwargs):
    requests = [{'text': text}]
    return send_requests('POST', '/predict', requests, max_predictions,
min_confidence, max_length, num_threads, cache, **kwargs)

def summarize_tasks(task_ids, max_predictions=10, min_confidence=0.1,
max_length=256, num_threads=1, cache=True, **kwargs):
    requests = [{'task_id': t} for t in task_ids]
    return send_requests('POST', '/summarize_tasks', requests,
max_predictions, min_confidence, max_length, num_threads, cache, **kwargs)

def send_request(url, method, payload=None):
    headers = {
        'Content-Type': 'application/json',
    }

    return (
        requests.request(
            method, url, data=json.dumps(payload), headers=headers
        )
        if payload is not None
        else requests.request(method, url, headers=headers)
    )

def predict(text, max_predictions=10, min_confidence=0.1, max_length=256,
num_threads=1, cache=True, **kwargs):
    requests = [{'text': text}]
    return send_requests('POST', '/predict', requests, max_predictions,
min_confidence, max_length, num_threads, cache, **kwargs)

def summarize_tasks(task_ids, max_predictions=10, min_confidence=0.1,
max_length=256, num_threads=1, cache=True, **kwargs):
    requests = [{'task_id': t} for t in task_ids]
    return send_requests('POST', '/summarize_tasks', requests,
max_predictions, min_confidence, max_length, num_threads, cache, **kwargs)

def send_batch_request(url, method, payloads):
    headers = {
        'Content-Type': 'application/json',
    }

    return (
        requests.request(
            method, url, data=json.dumps({'data': payloads}), headers=headers
        )
        if len(payloads) > 0
        else requests.request(method, url, headers=headers)
    )

def predict(text, max_predictions=10, min_confidence=0.1, max_length=256,
num_threads=1, cache=True, **kwargs):
    requests = [{'text': text}]
    return send_batch_requests('POST', '/predict', requests,
max_predictions, min_confidence, max_length, num_threads, cache, **kwargs)

def summarize_tasks(task_ids, max_predictions=10, min_confidence=0.1,
max_length=256, num_threads=1, cache=True, **kwargs):
    requests = [{'task_id': t} for t in task_ids]
    return send_batch_requests('POST', '/summarize_tasks', requests,
max_predictions, min_confidence, max_length, num_threads, cache, **kwargs)

def send_async_batch_request(url, method, payloads):
    if len(payloads) > 0:
        headers = {
            'Content-Type': 'application/json',
        }

                response = requests.request(method, url, data=json.dumps({'data':
        payloads}), headers=headers)
        response.raise_for_status()
        return response.text
    else:
        return None

def predict(text, max_predictions=10, min_confidence=0.1, max_length=256,
num_threads=1, cache=True, **kwargs):
    requests = [{'text': text}]
    return send_async_batch_requests('POST', '/predict', requests,
max_predictions, min_confidence, max_length, num_threads, cache, **kwargs)

def summarize_tasks(task_ids, max_predictions=10, min_confidence=0.1,
max_length=256, num_threads=1, cache=True, **kwargs):
    requests = [{'task_id': t} for t in task_ids]
    return send_async_batch_requests('POST', '/summarize_tasks', requests,
max_predictions, min_confidence, max_length, num_threads, cache, **kwargs)

def check_async_batch_status(task_id):
    url = f'/check/{task_id}'
    response = requests.get(url)
    return response.json()['done']

def predict(text, max_predictions=10, min_confidence=0.1, max_length=256,
num_threads=1, cache=True, **kwargs):
    requests = [{'text': text}]
    task_id = send_async_batch_requests('POST', '/predict', requests,
max_predictions, min_confidence, max_length, num_threads, cache, **kwargs)
    status = check_async_batch_status(task_id)
    while not status:
        time.sleep(0.1)
        status = check_async_batch_status(task_id)
    response = requests.get(f'/results/{task_id}')
    return response.json()['data']

def summarize_tasks(task_ids, max_predictions=10, min_confidence=0.1,
max_length=256, num_threads=1, cache=True, **kwargs):
    requests = [{'task_id': t} for t in task_ids]
    send_async_batch_requests('POST', '/summarize_tasks', requests,
max_predictions, min_confidence, max_length, num_threads, cache, **kwargs)
    statuses = {t: False for t in task_ids}
    while any(statuses.values()):
        time.sleep(0.1)
        new_statuses = {}
        for task_id in task_ids:
            url = f'/check/{task_id}'
            response = requests.get(url)
            status = response.json()['done']
            if status:
                url = f'/results/{task_id}'
                response = requests.get(url)
                data = response.json()['data']
                print(f"Task {task_id} done. Data: {data}")
            new_statuses[task_id] = status
        statuses = new_statuses