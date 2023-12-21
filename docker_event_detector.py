from docker import DockerClient
from redis import Redis
from json import dumps, loads
from base64 import b64encode

docker = DockerClient(base_url="unix:///var/run/docker.sock")
redis = Redis()

if docker.ping() is False:
    raise Exception("Docker Host Is NOT Available!")

events_object = docker.events()

while True:
    event = events_object.next()
    event_data = loads(event.decode("utf8"))
    event_encoded_data = b64encode(dumps(event_data).encode("ascii"))
    if event_data["Action"] == "create" and event_data["Type"] == "container":
        redis.publish("create_docker_container", event_encoded_data)
        print("Create Event Published.")
    if event_data["Action"] == "start" and event_data["Type"] == "container":
        redis.publish("start_docker_container", event_encoded_data)
        print("Start Event Published.")
