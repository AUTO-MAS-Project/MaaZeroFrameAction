#   MaaZeroFrameAction: A Zero Frame Action Tool for Arknights
#   Copyright © 2026 AUTO-MAS Team

#   This file is part of MaaZeroFrameAction.

#   MaaZeroFrameAction is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published
#   by the Free Software Foundation, either version 3 of the License,
#   or (at your option) any later version.

#   MaaZeroFrameAction is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty
#   of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
#   the GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with MaaZeroFrameAction. If not, see <https://www.gnu.org/licenses/>.

#   Contact: DLmaster_361@163.com


import os
import sys
import ctypes
import atexit
import psutil
import pyautogui
import tkinter as tk
from pathlib import Path
from tkinter import messagebox
from loguru import logger

from config import Config
from core import listener, ConnectTask, ConnectThread

logger.remove()
logger.add(
    sink=Path.cwd() / "debug/app.log",
    level="INFO",
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    enqueue=True,
    backtrace=True,
    diagnose=True,
    rotation="1 week",
    retention="1 month",
    compression="zip",
)
logger.add(
    sink=sys.stderr,
    level="DEBUG",
    format="<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <level>{message}</level>",
    enqueue=True,
    backtrace=True,
    diagnose=True,
    colorize=True,
)
if not ctypes.windll.shell32.IsUserAnAdmin():
    logger.error("请以管理员权限运行本程序")
    ctypes.windll.shell32.ShellExecuteW(
        None, "runas", sys.executable, os.path.realpath(sys.argv[0]), None, 1
    )
    sys.exit(0)


class KeyCapture:
    """按键捕获辅助类"""

    # 特殊按键映射
    SPECIAL_KEYS = {
        "space": "space",
        "Return": "enter",
        "BackSpace": "backspace",
        "Tab": "tab",
        "Escape": "esc",
        "Shift_L": "shift",
        "Shift_R": "shift",
        "Control_L": "ctrl",
        "Control_R": "ctrl",
        "Alt_L": "alt",
        "Alt_R": "alt",
        "Caps_Lock": "caps_lock",
        "Delete": "delete",
        "Insert": "insert",
        "Home": "home",
        "End": "end",
        "Page_Up": "page_up",
        "Page_Down": "page_down",
        "Up": "up",
        "Down": "down",
        "Left": "left",
        "Right": "right",
    }

    @staticmethod
    def normalize_key(key: str) -> str:
        """
        标准化按键名称

        Args:
            key: 原始按键名称

        Returns:
            str: 标准化后的按键名称
        """
        # 检查是否是特殊键
        if key in KeyCapture.SPECIAL_KEYS:
            return KeyCapture.SPECIAL_KEYS[key]

        # F1-F12
        if key.startswith("F") and len(key) <= 3:
            return key.lower()

        # 数字键盘
        if key.startswith("KP_"):
            return "num_" + key[3:].lower()

        # 普通字符键
        if len(key) == 1:
            return key.lower()

        return key.lower()


class SettingsWindow:
    """键位设置窗口"""

    # 配置项映射：(配置组, 配置名, 中文描述)
    CONFIG_ITEMS = [
        ("Key", "Pause", "暂停/继续划火柴"),
        ("Key", "SelectDeployable", "选中待部署区干员"),
        ("Key", "SelectDeployed", "选中已部署干员"),
        ("Key", "UseSkill", "释放技能"),
        ("Key", "Retreat", "撤退干员"),
        ("Key", "NextFrame", "下一帧"),
        ("Key", "AnotherQuit", "退出/暂停"),
    ]

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("明日方舟PC端划火柴工具")
        self.root.geometry("500x550")
        self.root.resizable(False, False)

        # 设置窗口图标
        icon_path = Path.cwd() / "res" / "MZFA.ico"
        if icon_path.exists():
            self.root.iconbitmap(icon_path)

        # 存储当前正在捕获的键位
        self.capturing_key = None

        # 存储Entry控件的引用
        self.entries = {}

        # 创建界面
        self._create_widgets()

        # 设置窗口关闭事件
        self.root.protocol("WM_DELETE_WINDOW", self._on_close)

        # 居中窗口
        self._center_window()

        # 启动状态更新（在主线程中）
        self._schedule_status_update()

    def _center_window(self):
        """将窗口居中显示"""
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def _create_widgets(self):
        """创建界面控件"""
        # 标题
        title_frame = tk.Frame(self.root)
        title_frame.pack(pady=15)

        title_label = tk.Label(
            title_frame,
            text="MaaZeroFrameAction",
            font=("Microsoft YaHei UI", 16, "bold"),
        )
        title_label.pack()

        subtitle_label = tk.Label(
            title_frame,
            text="点击输入框后按下想要设置的按键",
            font=("Microsoft YaHei UI", 9),
            fg="gray",
        )
        subtitle_label.pack()

        # 状态显示区域
        status_frame = tk.Frame(self.root)
        status_frame.pack(pady=10)

        status_text_label = tk.Label(
            status_frame,
            text="当前状态:",
            font=("Microsoft YaHei UI", 10),
        )
        status_text_label.pack(side=tk.LEFT, padx=5)

        self.status_label = tk.Label(
            status_frame,
            text="运行中",
            font=("Microsoft YaHei UI", 10, "bold"),
            fg="green",
            width=10,
        )
        self.status_label.pack(side=tk.LEFT)

        # 主内容区域
        content_frame = tk.Frame(self.root)
        content_frame.pack(pady=10, padx=30, fill=tk.BOTH, expand=True)

        # 创建每个配置项的输入行
        for group, name, description in self.CONFIG_ITEMS:
            self._create_key_setting_row(content_frame, group, name, description)

        # 按钮区域
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=15)

        reset_button = tk.Button(
            button_frame,
            text="恢复默认",
            command=self._reset_to_default,
            width=12,
            height=1,
            font=("Microsoft YaHei UI", 10),
        )
        reset_button.pack(side=tk.LEFT, padx=5)

    def _create_key_setting_row(
        self, parent: tk.Frame, group: str, name: str, description: str
    ):
        """
        创建单个键位设置行

        Args:
            parent: 父容器
            group: 配置组名
            name: 配置项名
            description: 中文描述
        """
        key_id = f"{group}.{name}"
        row_frame = tk.Frame(parent)
        row_frame.pack(fill=tk.X, pady=5)

        # 标签
        label = tk.Label(
            row_frame,
            text=description + ":",
            width=18,
            anchor="w",
            font=("Microsoft YaHei UI", 10),
        )
        label.pack(side=tk.LEFT, padx=(0, 10))

        # 输入框
        entry = tk.Entry(
            row_frame,
            width=15,
            font=("Microsoft YaHei UI", 10),
            justify="center",
            readonlybackground="white",
        )
        current_value = Config.get(group, name)
        entry.insert(0, current_value)
        entry.config(state="readonly")
        entry.pack(side=tk.LEFT, padx=5)

        # 绑定点击事件
        entry.bind(
            "<Button-1>", lambda e: self._start_capture(key_id, entry, group, name)
        )

        # 保存引用
        self.entries[key_id] = entry

    def _start_capture(self, key_id: str, entry: tk.Entry, group: str, name: str):
        """
        开始捕获按键

        Args:
            key_id: 配置标识 (group.name)
            entry: 对应的输入框控件
            group: 配置组名
            name: 配置项名
        """
        if self.capturing_key:
            # 如果已经在捕获其他按键，先取消之前的
            old_entry = self.entries[self.capturing_key[0]]
            old_entry.config(readonlybackground="white")

        self.capturing_key = (key_id, group, name)
        entry.config(readonlybackground="#FFEB3B")  # 黄色背景表示正在捕获

        # 设置全局标志，禁用监听器响应
        Config.is_capturing_key = True

        # 绑定键盘事件
        entry.focus_set()
        entry.bind("<KeyPress>", self._on_key_press)

    def _on_key_press(self, event):
        """
        按键按下事件处理

        Args:
            event: 键盘事件
        """
        if not self.capturing_key:
            return

        key_id, group, name = self.capturing_key

        # 标准化按键名称
        key = KeyCapture.normalize_key(event.keysym)

        # 检查是否与其他键位冲突
        for cfg_group, cfg_name, cfg_desc in self.CONFIG_ITEMS:
            cfg_key_id = f"{cfg_group}.{cfg_name}"
            if cfg_key_id != key_id and Config.get(cfg_group, cfg_name) == key:
                messagebox.showwarning(
                    "键位冲突",
                    f"按键 '{key}' 已被 '{cfg_desc}' 使用！",
                )
                # 恢复背景色
                self.entries[key_id].config(readonlybackground="white")
                self.capturing_key = None
                # 延迟300ms恢夏标志，给用户时间释放按键
                self.root.after(300, lambda: setattr(Config, "is_capturing_key", False))
                return "break"

        # 更新配置和显示
        Config.set(group, name, key)
        entry = self.entries[key_id]
        entry.config(state="normal")
        entry.delete(0, tk.END)
        entry.insert(0, key)
        entry.config(state="readonly", readonlybackground="white")

        # 取消绑定
        entry.unbind("<KeyPress>")
        self.capturing_key = None
        # 延迟300ms恢夏标志，给用户时间释放按键
        self.root.after(300, lambda: setattr(Config, "is_capturing_key", False))

        logger.info(f"已设置 {group}.{name} = {key}")

        return "break"  # 阻止事件继续传播

    def _reset_to_default(self):
        """恢复默认设置"""
        result = messagebox.askyesno(
            "确认恢复",
            "确定要恢复到默认键位设置吗？",
        )

        if result:
            # 恢复所有配置项到默认值
            for group, name, _ in self.CONFIG_ITEMS:
                # 获取ConfigItem的默认值
                config_item = getattr(Config, f"{group}_{name}")
                default_value = config_item.validator.default
                Config.set(group, name, default_value)

                # 更新UI
                key_id = f"{group}.{name}"
                entry = self.entries[key_id]
                entry.config(state="normal")
                entry.delete(0, tk.END)
                entry.insert(0, default_value)
                entry.config(state="readonly")

            logger.info("已恢复默认设置")
            messagebox.showinfo("成功", "已恢复默认键位设置")

    def _schedule_status_update(self):
        """定期更新状态（在主线程中）"""
        try:
            # 直接在这里更新，避免额外的函数调用
            if Config.paused:
                if self.status_label.cget("text") != "已暂停":
                    self.status_label.config(text="已暂停", fg="red")
            else:
                if self.status_label.cget("text") != "运行中":
                    self.status_label.config(text="运行中", fg="green")
            # 继续调度下一次更新
            self.root.after(1000, self._schedule_status_update)
        except:
            # 窗口已关闭，停止调度
            pass

    def _on_close(self):
        """窗口关闭事件"""

        logger.info("用户关闭设置窗口")

        ConnectTask.stop()
        listener.stop()
        listener.join()

        logger.info("程序退出")

        self.root.quit()

    def run(self):
        """运行GUI"""
        logger.info("启动设置界面")
        self.root.mainloop()
        # 销毁窗口
        try:
            self.root.destroy()
        except:
            pass


if __name__ == "__main__":

    pyautogui.PAUSE = 0
    pyautogui.FAILSAFE = False

    p = psutil.Process(os.getpid())
    p.nice(psutil.HIGH_PRIORITY_CLASS)

    if sys.platform == "win32":
        ctypes.windll.winmm.timeBeginPeriod(1)
        atexit.register(lambda: ctypes.windll.winmm.timeEndPeriod(1))

    logger.info("加载配置文件")
    Config.connect(Path.cwd() / "config/config.json")

    logger.info("启动任务线程")
    ConnectThread.start()
    listener.start()

    app = SettingsWindow()
    app.run()
