import json
import threading

from monitor.task import Task

def load_proxies(filename):
    proxies = []
    try:
        with open(filename) as file:
            for line in file:
                split_line = line.split(':')
                formatted_line = f"https://{split_line[2]}:{line[3]}@{line[0]}:{line[1]}"
                proxies.append(formatted_line.strip())
    except Exception as e:
        print(f"Error loading proxies: {e}")
    return proxies

def load_config(filename):
    try:
        with open(filename) as file:
            return json.load(file)
    except Exception as e:
        print(f"Error loading config: {e}")
        return None

def start_task(proxies, site, webhook, delay, task_id):
    task = Task(proxies, site, webhook, delay, task_id)
    task.monitor()

def main():
    config = load_config("config.json")
    if not config or not config.get("sites"):
        print("No sites registered or invalid config - check config.json")
        return

    proxies = load_proxies("proxies.txt")
    if not proxies:
        print("No proxies loaded or invalid proxies file - check proxies.txt")
        return

    delay = config["delay"]
    
    for task_id, (site, webhook) in enumerate(zip(config["sites"], config["webhooks"])):
        thread = threading.Thread(target=start_task, args=(proxies, site, webhook, delay, task_id))
        thread.start()

if __name__ == "__main__":
    main()

    



