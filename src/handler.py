import socketserver
import json

class Handler (socketserver.StreamRequestHandler):
	def send_message(self, message):
		if isinstance(message, tuple):
			message = '\n\r'.join(message)

		self.wfile.write(message.encode() + b'\r\n')

	def handle(self):
		self.send_welcome_message()
		self.serve()

	def send_welcome_message(self):
		m = (
			'Successfully connected.',
		)

		self.send_message(m)

	def get_action(self, choice: str):
		try:
			c = int(choice)
			return {
				1: self.serve,
				2: self.quit
			}[c]
		except (ValueError, KeyError):
			self.send_message(f'Invalid value: {choice}')
			return self.serve

	def serve(self):
		m = (
			'Whatcha wanna do?',
			'1: Ask me again',
			'2: Quit'
		)

		self.send_message(m)
		r = self.rfile.readline().strip(b'\n\r')
		self.get_action(r)()

	def quit(self):
		self.send_message('Bye bye 👋')
		self.finish()
