from docker import DockerClient
from redis import Redis
from json import loads
from base64 import b64decode

docker = DockerClient(base_url="unix:///var/run/docker.sock")
redis = Redis(decode_responses=True)

if docker.ping() is False:
    raise Exception("Docker Host Is NOT Available!")

event_channel = redis.pubsub()
event_channel.subscribe("start_docker_container")

for message in event_channel.listen():
    if message["type"] == "message":
        event_data = loads(b64decode(message["data"]).decode("utf8"))
        if event_data["Actor"]["Attributes"]["image"].endswith(":latest") is True:
            container = docker.containers.get(event_data["Actor"]["Attributes"]["name"])
            container.remove(force=True)
            print(f"container {event_data['Actor']['Attributes']['name']} removed due to our docker policies.")
