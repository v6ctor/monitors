import json
import threading

from monitor.task import Task

try:
    with open("config.json") as data:
        raw = json.load(data)
        data.close()

    with open("proxies.txt") as data:
        proxies = []
        for line in data:
            split_line = line.split(':')
            formatted_line = 'https://' + split_line[2] + ':' + line[3] + '@' + line[0] + ':' + line[1]
            proxies.append(formatted_line.replace('\n','')) 
except Exception as e:
    print(e)
    exit()

if raw["sites"] == []:
    print("No sites registered - check sites.json")

def start(proxies, site, webhook, delay, task_id):
    task = Task(proxies, site, webhook, delay, task_id)
    task.test()

def main():
    for index in range(len(raw["sites"])):
        task = threading.Thread(target = start, args = (proxies, raw["sites"][index], raw["webhooks"][index], raw["delay"], index,))
        task.start()

if __name__ == "__main__":
    main()

    



