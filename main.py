#   AUTO-MAS: A Multi-Script, Multi-Config Management and Automation Software
#   Copyright © 2026 AUTO-MAS Team

#   This file is part of AUTO-MAS.

#   AUTO-MAS is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published
#   by the Free Software Foundation, either version 3 of the License,
#   or (at your option) any later version.

#   AUTO-MAS is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty
#   of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See
#   the GNU General Public License for more details.

#   You should have received a copy of the GNU General Public License
#   along with AUTO-MAS. If not, see <https://www.gnu.org/licenses/>.

#   Contact: DLmaster_361@163.com

import os
import sys
import time
import json
import ctypes
import psutil
import atexit
import asyncio
import argparse
import win32gui
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


(Path.cwd() / "debug").mkdir(parents=True, exist_ok=True)
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

        global config

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

        global config

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

        global config

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

        global config

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

        global config

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

        global config

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

        global config

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


(Path.cwd() / "maa_option.json").write_text(
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


listener: keyboard.Listener | None = None
exit_event = asyncio.Event()


def on_key_release(key: keyboard.Key | keyboard.KeyCode | None) -> None:
    """pynput 回调"""

    if isinstance(key, keyboard.KeyCode):
        k = key.char.lower() if key.char else key.vk
    elif isinstance(key, keyboard.Key):
        k = key.name.lower()
    else:
        return

    global arknights_hwnd, config

    if k == config["exit-key"]:
        logger.info("检测到退出按键，准备退出程序")
        exit_event.set()

    if arknights_hwnd == 0 or not tasker.inited:
        logger.warning("未检测到明日方舟窗口或任务器未初始化，按键操作无效")
        return

    if k == config["advance-select-deployable-key"]:
        logger.info("触发选中待部署区干员")
        tasker.post_task("选中待部署区干员")
    elif k == config["advance-select-deployed-key"]:
        logger.info("触发选中已部署干员")
        tasker.post_task("选中已部署干员")
    elif k == config["advance-skill-key"]:
        logger.info("触发释放技能")
        tasker.post_task("释放技能")
    elif k == config["advance-retreat-key"]:
        logger.info("触发撤退干员")
        tasker.post_task("撤退干员")
    elif k == config["next-frame-key"]:
        logger.info("触发下一帧")
        tasker.post_task("下一帧")
    elif k == config["another-quit-key"]:
        logger.info("触发退出/暂停额外键位")
        pyautogui.press("esc")


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


async def main():
    """主程序"""

    logger.info("程序启动")

    global listener, arknights_hwnd, tasker

    listener = keyboard.Listener(on_release=on_key_release)
    listener.start()

    try:
        while not exit_event.is_set():

            new_hwnd = win32gui.FindWindow(None, "明日方舟")

            if arknights_hwnd != new_hwnd:

                arknights_hwnd = new_hwnd

                if new_hwnd == 0:

                    logger.warning("未检测到明日方舟窗口，暂停任务器")

                else:

                    reconnect_arknights(new_hwnd)

            if not tasker.inited:

                reconnect_arknights(arknights_hwnd)

            await asyncio.sleep(1)

    except KeyboardInterrupt:
        pass
    finally:
        listener.stop()
        listener.join()
        logger.info("程序退出")


config = {}

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="划火柴基础工具")
    parser.add_argument(
        "--exit-key",
        type=str,
        default="f10",
        help="指定退出程序的按键，默认f10。例如: --exit-key f10",
    )
    parser.add_argument(
        "--advance-select-deployable-key",
        type=str,
        default="s",
        help="指定0帧选中待部署区干员的按键，默认s。例如: --advance-select-deployable-key s",
    )
    parser.add_argument(
        "--advance-select-deployed-key",
        type=str,
        default="w",
        help="指定0帧选中已部署干员的按键，默认w。例如: --advance-select-deployed-key w",
    )
    parser.add_argument(
        "--advance-skill-key",
        type=str,
        default="r",
        help="指定0帧释放技能的按键，默认r。例如: --advance-skill-key r",
    )
    parser.add_argument(
        "--advance-retreat-key",
        type=str,
        default="t",
        help="指定0帧撤退干员的按键，默认t。例如: --advance-retreat-key t",
    )
    parser.add_argument(
        "--next-frame-key",
        type=str,
        default="f",
        help="指定下一帧的按键，默认f。例如: --next-frame-key f",
    )
    parser.add_argument(
        "--another-quit-key",
        type=str,
        default="space",
        help="指定另一个退出/暂停按键，默认space。例如: --another-quit-key space",
    )

    args = parser.parse_args()

    config = {
        "exit-key": args.exit_key.lower(),
        "advance-select-deployable-key": args.advance_select_deployable_key.lower(),
        "advance-select-deployed-key": args.advance_select_deployed_key.lower(),
        "advance-skill-key": args.advance_skill_key.lower(),
        "advance-retreat-key": args.advance_retreat_key.lower(),
        "next-frame-key": args.next_frame_key.lower(),
        "another-quit-key": args.another_quit_key.lower(),
    }

    pyautogui.PAUSE = 0
    pyautogui.FAILSAFE = False

    p = psutil.Process(os.getpid())
    p.nice(psutil.HIGH_PRIORITY_CLASS)

    if sys.platform == "win32":
        ctypes.windll.winmm.timeBeginPeriod(1)
        atexit.register(lambda: ctypes.windll.winmm.timeEndPeriod(1))

    asyncio.run(main())
