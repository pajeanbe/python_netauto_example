import yaml
from netmiko import ConnectHandler
from pathlib import Path
import logging

# Set up logging for better error tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_yaml_file(path):
    try:
        with open(path, 'r') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        logger.error(f"YAML file not found: {path}")
        return {}
    except yaml.YAMLError as e:
        logger.error(f"Error parsing YAML file {path}: {e}")
        return {}
    except Exception as e:
        logger.error(f"Unexpected error loading YAML file {path}: {e}")
        return {}

def load_hc_script(path):
    try:
        with open(path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        logger.error(f"Script file not found: {path}")
        return ""
    except Exception as e:
        logger.error(f"Error loading script file {path}: {e}")
        return ""

def main():
    try:
        hosts = load_yaml_file(Path('./inventory.yaml'))
        if len(hosts) == 0:
            print("No hosts found")
            return

        commands_text = load_hc_script(Path('./hc_script.txt'))
        if not commands_text:
            print("No commands found in script file")
            return

        # Split commands into individual lines and filter out empty lines
        commands = [cmd.strip() for cmd in commands_text.splitlines() if cmd.strip()]

        for host in hosts:
            try:
                # Use context manager for proper connection cleanup
                with ConnectHandler(**host) as net_connect:
                    logger.info(f"Connected to {host.get('host', 'unknown host')}")

                    for command in commands:
                        try:
                            output = net_connect.send_command(command)
                            print(f"Command: {command}")
                            print(f"Output: {output}")
                            print("-" * 50)
                        except Exception as e:
                            logger.error(f"Error executing command '{command}' on {host.get('host', 'unknown host')}: {e}")

            except Exception as e:
                logger.error(f"Connection error for host {host.get('host', 'unknown host')}: {e}")

    except KeyboardInterrupt:
        print("\nOperation cancelled by user")
    except Exception as e:
        logger.error(f"Unexpected error in main: {e}")

if __name__ == "__main__":
    main()