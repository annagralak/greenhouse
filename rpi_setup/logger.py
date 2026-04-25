import json
import os
import time
from threading import Lock


class Logger:
	"""Singleton JSON logger writing topic-based entries."""

	_instance = None
	_lock = Lock()

	def __new__(cls, *args, **kwargs):
		"""Ensure single instance."""

		with cls._lock:
			if cls._instance is None:
				cls._instance = super().__new__(cls)
				cls._instance._initialized = False
		return cls._instance

	def __init__(self, base_filename="data", folder="data"):
		"""Initialize log file once."""

		if self._initialized:
			return

		self._file_lock = Lock()

		# Timestamped filename
		timestamp = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
		self.filename = os.path.join(folder, f"{base_filename}_{timestamp}.json")

		os.makedirs(os.path.dirname(self.filename) or ".", exist_ok=True)

		# Create empty file
		with open(self.filename, "w") as f:
			pass

		self._initialized = True

	def _extract_timestamp(self, data: dict):
		"""Return timestamp from first sensor entry."""

		for v in data.values():
			if isinstance(v, dict) and "timestamp" in v:
				return v["timestamp"]
			return None

	def log(self, topic: str, data: dict):
		"""Append log entry with topic, data, and timestamp."""

	    # Extract timestamp from StateStore-enriched data
		timestamp = self._extract_timestamp(data)
		
		entry = {
	        "topic": topic,
	        "data": data,
	        "timestamp": timestamp
	    }

		with self._file_lock:
			with open(self.filename, "a", encoding="utf-8") as f:
				f.write(json.dumps(entry, ensure_ascii=False) + "\n")

