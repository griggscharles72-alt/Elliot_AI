#!/usr/bin/env python3
"""
Personality Module: Handles AI personality responses and command processing.
"""

class Personality:
    def __init__(self, name="SABLE"):
        self.name = name

    def respond(self, command: str) -> str:
        """
        Process a command string and return a response.
        This is a placeholder: expand with real logic as needed.
        """
        command = command.strip()
        if not command:
            return "[Personality] No command received."
        return f"[{self.name}] Command received: {command}"
