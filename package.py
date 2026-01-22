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
import maa

version = "0.0.0.0"

maa_path = os.path.dirname(maa.__file__)
bin_path = os.path.join(maa_path, "bin")
os.system(
    "powershell -Command python -m nuitka --standalone --onefile --mingw64"
    f' --enable-plugins=tk-inter --include-raw-dir="{bin_path}"=maa/bin'
    " --windows-console-mode=attach --windows-uac-admin"
    " --onefile-tempdir-spec='{TEMP}\\MZFA'"
    " --windows-icon-from-ico=res\\MZFA.ico"
    " --company-name='AUTO-MAS Team' --product-name=MaaZeroFrameAction"
    f" --file-version={version}"
    f" --product-version={version}"
    " --file-description='MaaZeroFrameAction Component'"
    " --copyright='Copyright © 2026 AUTO-MAS Team'"
    " --assume-yes-for-downloads --output-filename=MaaZeroFrameAction"
    " --remove-output main.py"
)
