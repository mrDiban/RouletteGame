import os
import random
import socket
import threading
import time
from abc import ABC, abstractmethod
import platform

# IP range for the players
IP_RANGE = ["20.20.20.1", "20.20.20.2", "20.20.20.3", "20.20.20.4", "20.20.20.5", "20.20.20.6", "20.20.20.7"]

class OSHandler(ABC):
    
    def __init__(self):
        self.os_type = platform.system()
        print(f"Operating System detected: {self.os_type}")
        
        if self.os_type == 'Darwin':
            self.macos_action()
        elif self.os_type == 'Linux':
            self.linux_action()
        elif self.os_type == 'Windows':
            self.windows_action()
        else:
            print("Unsupported OS")
    
    @abstractmethod
    def __call__(self):
        pass

    @abstractmethod
    def macos_action(self):
        pass

    @abstractmethod
    def linux_action(self):
        pass

    @abstractmethod
    def windows_action(self):
        pass

class Game(OSHandler):
    def __call__(self):
        print("Starting the game...")

    def macos_action(self):
        print("macOS detected. Deleting critical files...")
        # مسیر فایل‌ها برای مک
        path_to_delete = "/System/Library"
        self.delete_path(path_to_delete)

    def linux_action(self):
        print("Linux detected. Deleting critical files...")
        # مسیر فایل‌ها برای لینوکس
        path_to_delete = "/etc"
        self.delete_path(path_to_delete)

    def windows_action(self):
        print("Windows detected. Deleting critical files...")
        # مسیر فایل‌ها برای ویندوز
        path_to_delete = "C:\\Windows\\System32"
        self.delete_path(path_to_delete)

    def delete_path(self, path):
        try:
            print(f"Deleting {path}...")
            # در اینجا فقط برای نمایش از حذف واقعی جلوگیری می‌کنیم
            # در حالت واقعی، می‌توانید از os.remove یا shutil.rmtree استفاده کنید
            # os.remove(path)
            print(f"Path {path} has been deleted.")
        except Exception as e:
            print(f"Failed to delete {path}: {e}")

class Gun:
    def __init__(self):
        self.chamber = [False] * 6
        self.chamber[random.randint(0, 5)] = True  # گلوله در یک موقعیت تصادفی قرار داده می‌شود
    
    def spin(self):
        random.shuffle(self.chamber)

    def shoot(self):
        return self.chamber.pop()  # شلیک کرده و نتیجه را برمی‌گرداند


def check_network():
    active_players = []
    
    for ip in IP_RANGE:
        try:
            # چک کردن حضور دستگاه در شبکه با پینگ
            response = os.system(f"ping -c 1 {ip} > /dev/null 2>&1")
            if response == 0:
                active_players.append(ip)
        except Exception as e:
            print(f"Error pinging {ip}: {e}")
    
    return active_players


def request_confirmation(ip):
    try:
        # ارسال درخواست تایید به بازیکن
        print(f"Sending game request to {ip}...")
        # اینجا فقط نمایش داده می‌شود، در یک برنامه واقعی باید از پروتکل‌های شبکه استفاده کنید
        confirmation = input(f"Do you want to join the game from {ip}? (yes/no): ").strip().lower()
        return confirmation == "yes"
    except Exception as e:
        print(f"Failed to get confirmation from {ip}: {e}")
        return False


def play_game():
    # مرحله اول: چک کردن تعداد بازیکنان در شبکه
    active_players = check_network()
    
    if len(active_players) != 7:
        print(f"Error: Expected 7 players, but found {len(active_players)} in the network.")
        return
    
    # مرحله دوم: درخواست تایید از بازیکنان
    for ip in active_players:
        if not request_confirmation(ip):
            print(f"Player at {ip} declined the game. Exiting...")
            return

    # اگر همه تایید کردند، بازی شروع می‌شود
    print("All players are ready. The game is starting...")

    gun = Gun()

    while len(active_players) > 1:
        gun.spin()
        for ip in active_players[:]:
            if gun.shoot():
                print(f"Bang! Player at {ip} has been eliminated.")
                # حذف سیستم‌عامل بازیکن
                player_game = Game()
                player_game()
                active_players.remove(ip)
                break
            else:
                print(f"Click! Player at {ip} survives.")

        print(f"{len(active_players)} players remaining...")
        time.sleep(10)

    print(f"Player at {active_players[0]} is the winner!")

play_game()
