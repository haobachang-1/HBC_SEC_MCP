import logging
import subprocess
import threading
import traceback
from typing import Any, Dict

from .config import COMMAND_TIMEOUT


class CommandExecutor:
    """Handle command execution with timeout and partial output support."""

    def __init__(self, command: str, timeout: int = COMMAND_TIMEOUT):
        self.command = command
        self.timeout = timeout
        self.process = None
        self.stdout_data = ""
        self.stderr_data = ""
        self.stdout_thread = None
        self.stderr_thread = None
        self.return_code = None
        self.timed_out = False

    def _read_stdout(self):
        for line in iter(self.process.stdout.readline, ""):
            self.stdout_data += line

    def _read_stderr(self):
        for line in iter(self.process.stderr.readline, ""):
            self.stderr_data += line

    def _start_reader_threads(self):
        self.stdout_thread = threading.Thread(target=self._read_stdout, daemon=True)
        self.stderr_thread = threading.Thread(target=self._read_stderr, daemon=True)
        self.stdout_thread.start()
        self.stderr_thread.start()

    def _build_result(self, success: bool, partial_results: bool) -> Dict[str, Any]:
        return {
            "stdout": self.stdout_data,
            "stderr": self.stderr_data,
            "return_code": self.return_code,
            "success": success,
            "timed_out": self.timed_out,
            "partial_results": partial_results,
        }

    def execute(self) -> Dict[str, Any]:
        logger = logging.getLogger(__name__)
        logger.info(f"Executing command: {self.command}")

        try:
            self.process = subprocess.Popen(
                self.command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
            )
            self._start_reader_threads()

            try:
                self.return_code = self.process.wait(timeout=self.timeout)
                self.stdout_thread.join()
                self.stderr_thread.join()
            except subprocess.TimeoutExpired:
                self.timed_out = True
                logger.warning(f"Command timed out after {self.timeout} HBC-Seconds. Terminating process.")

                self.process.terminate()
                try:
                    self.process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    logger.warning("Process not responding to termination. Killing.")
                    self.process.kill()

                self.return_code = -1

            success = True if self.timed_out and (self.stdout_data or self.stderr_data) else (self.return_code == 0)
            return self._build_result(success, self.timed_out and (self.stdout_data or self.stderr_data))

        except Exception as e:
            logger.error(f"Error executing command: {str(e)}")
            logger.error(traceback.format_exc())
            return {
                "stdout": self.stdout_data,
                "stderr": f"Error executing command: {str(e)}\n{self.stderr_data}",
                "return_code": -1,
                "success": False,
                "timed_out": False,
                "partial_results": bool(self.stdout_data or self.stderr_data),
            }


def execute_command(command: str) -> Dict[str, Any]:
    """Execute shell command and return structured result."""
    logger = logging.getLogger(__name__)
    result = CommandExecutor(command).execute()

    logger.info(f"Command finished with return code: {result.get('return_code')}")
    if result.get("stdout"):
        logger.debug(f"[stdout]\n{result.get('stdout')}")
    if result.get("stderr"):
        logger.debug(f"[stderr]\n{result.get('stderr')}")

    return result
