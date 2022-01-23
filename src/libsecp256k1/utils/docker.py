import subprocess

class Docker:

	@classmethod
	def exec(self, child_command: str, *args: str) -> dict:
		command = child_command.split(' ')
		command.extend(args)
		process = subprocess.run(command,
			stdout=subprocess.PIPE,stderr=subprocess.PIPE)
		print(process.stdout.decode())
		returncode = process.returncode
		if returncode == 0:
			return {'status': 200, 'message': 'Execute {} successful.'.format(child_command), 'errcode': None}
		else:
			return {'status': 400, 'message': 'Error: Failed to execute {}.'.format(child_command), 'errcode': str(process.stderr)}
