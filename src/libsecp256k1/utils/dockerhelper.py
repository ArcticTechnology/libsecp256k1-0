from concurrent.futures import process
from re import sub
import shlex; import subprocess
from turtle import st

class DockerHelper:
	# Docker:
	#sudo apt-get update
	#sudo apt install docker.io

	#sudo docker version
	#sudo docker images
	#sudo docker build -t libsecp-builder .
	#sudo docker run -it --rm -v "`pwd`/build:/libsecp/compiled" --name libsecp-builder-instance libsecp-builder
	#sudo docker run hello-docker

	@classmethod
	def build(self, path, *args):
		arglex = shlex.quote(' '.join(args))
		command = shlex.split('docker build {a} {p}'.format(a=arglex,p=path))
		process = subprocess.run(command,
			stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		returncode = process.returncode
		if returncode == 0:
			return {'status': 200, 'message': 'Docker build successful.'}
		else:
			return {'status': 400, 'message': 'Error: Failed to build Docker.'}

