"""
Quick test - Menu only (không train AI)
"""
import sys
import os

# Add parent dir to path
sys.path.insert(0, os.path.dirname(__file__))

from ui.menu import show_menu

if __name__ == "__main__":
    print("Testing menu system...")
    choice = show_menu()
    print(f"Selected: {choice}")
