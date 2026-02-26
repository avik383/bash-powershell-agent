import subprocess
import os
from config import ALLOWED_COMMANDS as default_allowed_commands

class Bash:
    
    def __init__(self, cwd: str, allowed_commands: List[str] = default_allowed_commands):
        self.cwd = cwd
        self.allowed_commands = allowed_commands

    def exec_bash_command(self, cmd: str) -> Dict[str, str]:
        if cmd:
            if cmd.split()[0] in self.allowed_commands:
                return self._run_bash_command(cmd)
            else:
                return {"Error": "This command is not allowed"}
        else:
            return {"Error": "No command provided"}

    def to_json_schema(self) -> Dict[str, Any]:
        return {
            "type": "function",
            "function": {
                "name": "exec_bash_command",
                "description": "Executes a bash command",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "cmd": {
                            "type": "string",
                            "description": "Bash command to execute"
                        }
                    },
                    "required": ["cmd"]
                }
            }
        }

    def _run_bash_command(self, cmd: str) -> Dict[str, str]:
        stdout, stderr, new_cwd = "", "", self.cwd
        try:
            full_cmd = f"{cmd};echo __END__;(pwd).Path"
            result = subprocess.run(
                ["powershell", "-NoProfile", "-Command", full_cmd],
                cwd=self.cwd, capture_output=True, text=True
            )
            
            stderr = result.stderr.strip()
            admin_stdout = result.stdout.split("__END__")
            stdout = admin_stdout[0].strip()
            print()
            print("Admin stdout")
            print(admin_stdout)
            print()

            if not stdout and not stderr:
                stdout = "[Command executed successfully with no output.]"
            if admin_stdout[-1].strip():
                self.cwd = admin_stdout[-1].strip()
            print()
            print("self.cwd")
            print(self.cwd)
            print()

        except Exception as e:
            stdout = ""
            stderr = str(e)

        return {"stdout": stdout, "stderr": stderr, "cwd": self.cwd}