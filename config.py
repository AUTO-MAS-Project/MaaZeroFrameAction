#   MaaZeroFrameAction: A Multi-Script, Multi-Config Management and Automation Software
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


from ConfigBase import ConfigBase, ConfigItem, KeyValidator


class _Config(ConfigBase):
    """全局配置"""

    Key_Pause = ConfigItem("Key", "Pause", "f10", KeyValidator("f10"))
    Key_SelectDeployable = ConfigItem("Key", "SelectDeployable", "s", KeyValidator("s"))
    Key_SelectDeployed = ConfigItem("Key", "SelectDeployed", "w", KeyValidator("w"))
    Key_UseSkill = ConfigItem("Key", "UseSkill", "r", KeyValidator("r"))
    Key_Retreat = ConfigItem("Key", "Retreat", "t", KeyValidator("t"))
    Key_NextFrame = ConfigItem("Key", "NextFrame", "f", KeyValidator("f"))
    Key_AnotherQuit = ConfigItem("Key", "AnotherQuit", "space", KeyValidator("space"))

    def __init__(self):
        super().__init__()

        self.paused: bool = False
        self.is_capturing_key: bool = False

    def keys(self) -> list[str]:
        """获取所有热键配置"""

        keys = []
        for name in dir(self):
            item = getattr(self, name)
            if isinstance(item, ConfigItem):
                keys.append(str(item.getValue()))

        return keys


Config = _Config()
