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


import time
import json
import win32gui
import threading
import pyautogui
from loguru import logger
from pynput import keyboard
from pathlib import Path

from maa.tasker import Tasker
from maa.toolkit import Toolkit
from maa.context import Context
from maa.resource import Resource
from maa.controller import (
    Win32Controller,
    MaaWin32ScreencapMethodEnum,
    MaaWin32InputMethodEnum,
)
from maa.custom_action import CustomAction

from config import Config


(Path.cwd() / "config").mkdir(parents=True, exist_ok=True)
(Path.cwd() / "debug").mkdir(parents=True, exist_ok=True)


resource = Resource()


@resource.custom_action("Play Select Deployable")
class PlaySelectDeployable(CustomAction):

    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:

        logger.info("开始执行战斗时选中待部署区干员动作")

        try:
            pyautogui.move(0, -10)
            pyautogui.press("esc")
            sleep(16)
            pyautogui.move(0, 10)
        except Exception as e:
            logger.exception(f"执行战斗时选中待部署区干员动作时出错：{e}")
            return False

        logger.success("成功执行战斗时选中待部署区干员动作")
        return True


@resource.custom_action("Pause Select Deployable")
class PauseSelectDeployable(CustomAction):

    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:

        logger.info("开始执行暂停时选中待部署区干员动作")

        try:
            pyautogui.press("esc")
            sleep(17)
            pyautogui.move(0, -10)
            pyautogui.press("esc")
            sleep(17)
            pyautogui.move(0, 10)
        except Exception as e:
            logger.exception(f"执行暂停时选中待部署区干员动作时出错：{e}")
            return False

        logger.success("成功执行暂停时选中待部署区干员动作")
        return True


@resource.custom_action("Play Select Deployed")
class PlaySelectDeployed(CustomAction):

    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:

        logger.info("开始执行战斗时选中已部署干员动作")

        try:
            pyautogui.click()
            pyautogui.press("esc")

        except Exception as e:
            logger.exception(f"执行战斗时选中已部署干员动作时出错：{e}")
            return False

        logger.success("成功执行战斗时选中已部署干员动作")
        return True


@resource.custom_action("Pause Select Deployed")
class PauseSelectDeployed(CustomAction):

    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:

        logger.info("开始执行暂停时选中已部署干员动作")

        try:
            pyautogui.press("esc")
            sleep(17)
            pyautogui.click()
            pyautogui.press("esc")

        except Exception as e:
            logger.exception(f"执行暂停时选中已部署干员动作时出错：{e}")
            return False

        logger.success("成功执行暂停时选中已部署干员动作")
        return True


@resource.custom_action("Play Skill")
class PlaySkill(CustomAction):

    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:

        logger.info("开始执行战斗时释放技能动作")
        try:
            pyautogui.click()
            pyautogui.press("esc")

        except Exception as e:
            logger.exception(f"执行战斗时释放技能动作时出错：{e}")
            return False

        logger.success("成功执行战斗时释放技能动作")
        return True


@resource.custom_action("Pause Skill")
class PauseSkill(CustomAction):

    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:

        logger.info("开始执行暂停时释放技能动作")

        try:
            pyautogui.press("esc")
            sleep(17)
            pyautogui.click()
            pyautogui.press("esc")
            time.sleep(1)

        except Exception as e:
            logger.exception(f"执行暂停时释放技能动作时出错：{e}")
            return False

        logger.success("成功执行暂停时释放技能动作")
        return True


@resource.custom_action("Play Retreat")
class PlayRetreat(CustomAction):

    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:

        logger.info("开始执行战斗时撤退干员动作")

        try:
            pyautogui.click()
            pyautogui.press("esc")

        except Exception as e:
            logger.exception(f"执行战斗时撤退干员动作时出错：{e}")
            return False

        logger.success("成功执行战斗时撤退干员动作")
        return True


@resource.custom_action("Pause Retreat")
class PauseRetreat(CustomAction):

    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:

        logger.info("开始执行暂停时撤退干员动作")

        try:
            pyautogui.press("esc")
            sleep(17)
            pyautogui.click()
            pyautogui.press("esc")

        except Exception as e:
            logger.exception(f"执行暂停时撤退干员动作时出错：{e}")
            return False

        logger.success("成功执行暂停时撤退干员动作")
        return True


@resource.custom_action("Next Frame 0.2x")
class NextFrame_0_2x(CustomAction):

    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:

        logger.info("开始执行0.2倍速下一帧动作")

        try:
            pyautogui.press("esc")
            sleep(165)
            pyautogui.press("esc")

        except Exception as e:
            logger.exception(f"执行0.2倍速下一帧动作时出错：{e}")
            return False

        logger.success("成功执行0.2倍速下一帧动作")
        return True


@resource.custom_action("Next Frame 1x")
class NextFrame_1x(CustomAction):

    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:

        logger.info("开始执行1倍速下一帧动作")

        try:
            pyautogui.press("esc")
            sleep(32)
            pyautogui.press("esc")

        except Exception as e:
            logger.exception(f"执行1倍速下一帧动作时出错：{e}")
            return False

        logger.success("成功执行1倍速下一帧动作")
        return True


@resource.custom_action("Next Frame 2x")
class NextFrame_2x(CustomAction):

    def run(self, context: Context, argv: CustomAction.RunArg) -> bool:

        logger.info("开始执行2倍速下一帧动作")

        try:
            pyautogui.press("esc")
            sleep(17)
            pyautogui.press("esc")

        except Exception as e:
            logger.exception(f"执行2倍速下一帧动作时出错：{e}")
            return False

        logger.success("成功执行2倍速下一帧动作")
        return True


def sleep(ms: float):
    """高精度忙等待函数，目标精度 ±0.1ms"""

    end = time.perf_counter() + ms / 1000.0
    while time.perf_counter() < end:
        pass


(Path.cwd() / "config/maa_option.json").write_text(
    json.dumps(
        {
            "logging": True,
            "save_draw": False,
            "stdout_level": 2,
            "save_on_error": False,
            "draw_quality": 85,
        },
        ensure_ascii=False,
        indent=4,
    ),
    encoding="utf-8",
)
Toolkit.init_option(Path.cwd())

resource.post_bundle(Path.cwd() / "res").wait()

arknights_hwnd = -1

tasker = Tasker()


def on_key_release(key: keyboard.Key | keyboard.KeyCode | None) -> None:
    """pynput 回调"""

    if Config.is_capturing_key:
        return

    if isinstance(key, keyboard.KeyCode):
        k = key.char.lower() if key.char else key.vk
    elif isinstance(key, keyboard.Key):
        k = key.name.lower()
    else:
        return

    global arknights_hwnd, tasker

    if k == Config.get("Key", "Pause"):
        logger.info("触发暂停键位")
        Config.paused = not Config.paused
        if Config.paused:
            logger.info("已暂停")
        else:
            logger.info("已恢复")
        return

    if Config.paused:
        return

    if k in Config.keys() and (arknights_hwnd == 0 or not tasker.inited):
        logger.warning("未检测到明日方舟窗口或任务器未初始化，按键操作无效")
        return

    if k == Config.get("Key", "SelectDeployable"):
        logger.info("触发选中待部署区干员")
        tasker.post_task("选中待部署区干员")
    elif k == Config.get("Key", "SelectDeployed"):
        logger.info("触发选中已部署干员")
        tasker.post_task("选中已部署干员")
    elif k == Config.get("Key", "UseSkill"):
        logger.info("触发释放技能")
        tasker.post_task("释放技能")
    elif k == Config.get("Key", "Retreat"):
        logger.info("触发撤退干员")
        tasker.post_task("撤退干员")
    elif k == Config.get("Key", "NextFrame"):
        logger.info("触发下一帧")
        tasker.post_task("下一帧")
    elif k == Config.get("Key", "AnotherQuit"):
        logger.info("触发退出/暂停额外键位")
        pyautogui.press("esc")


listener = keyboard.Listener(on_release=on_key_release)


def reconnect_arknights(hwnd: int):
    """重新连接明日方舟"""

    global controller, tasker

    controller = Win32Controller(
        hWnd=hwnd,
        screencap_method=MaaWin32ScreencapMethodEnum.FramePool,
        mouse_method=MaaWin32InputMethodEnum.PostMessageWithCursorPos,
    )
    controller.post_connection().wait()
    tasker.bind(resource, controller)

    if tasker.inited:
        logger.success("重新连接成功")
    else:
        logger.error("重新连接失败")


class _ConnectTask:
    def __init__(self):

        self.stop_event = threading.Event()

    def run(self):

        global arknights_hwnd

        while not self.stop_event.is_set():

            new_hwnd = win32gui.FindWindow(None, "明日方舟")

            if arknights_hwnd != new_hwnd:

                arknights_hwnd = new_hwnd

                if new_hwnd == 0:

                    logger.warning("未检测到明日方舟窗口，暂停任务器")

                else:

                    reconnect_arknights(new_hwnd)

            if not tasker.inited:

                reconnect_arknights(arknights_hwnd)

            time.sleep(1)

    def stop(self):
        """发送停止信号的方法"""
        self.stop_event.set()


ConnectTask = _ConnectTask()
ConnectThread = threading.Thread(target=ConnectTask.run, daemon=True)
