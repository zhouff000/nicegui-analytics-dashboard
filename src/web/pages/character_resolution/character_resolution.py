import streamlit as st
from src.web.utils.i18n_utils import I18N

i18n = I18N("locales", st.session_state.lang)

i18n.set_scope("character_resolution")
st.markdown(
    """
    ## nmcli
### 连接 Wi-Fi 命令备忘录

| 任务              | 命令                                                   |
| --------------- | ---------------------------------------------------- |
| **扫描网络**        | `nmcli device wifi list`                             |
| **连接网络**        | `sudo nmcli dev wifi connect "SSID" password "PASS"` |
| **查看活动连接**      | `nmcli con show --active`                            |
| **查看所有已存连接**    | `nmcli con show`                                     |
| **断开连接**        | `sudo nmcli dev disconnect wlan0`                    |
| **连接已存网络**      | `sudo nmcli con up "连接名"`                            |
| **删除已存网络**      | `sudo nmcli con del "连接名"`                           |
| **关闭/开启 Wi-Fi** | `nmcli radio wifi off/on`                            |

### **方法一：使用 `nmcli` 创建热点 (推荐)**
`nmcli` 是 NetworkManager 的命令行客户端，是管理网络连接的现代标准。用它来创建热点相对简单直观。
#### **步骤 1：确保 NetworkManager 正在管理您的无线设备**
Ubuntu Server 24.04 默认使用 `netplan` 来配置网络，而 `netplan` 后端可以是 `systemd-networkd` 或 `NetworkManager`。要使用 `nmcli`，我们需要确保 `NetworkManager` 拥有对无线网卡的控制权。
1. 检查 netplan 配置：查看 /etc/netplan/ 目录下的 .yaml 配置文件。
```bash
#
# 查看 netplan 配置文件内容
#
cat /etc/netplan/*.yaml
```

确保 `renderer` 设置为 `NetworkManager`，或者为您的无线设备 (`wifis`) 指定 `renderer: NetworkManager`。

**示例配置 `/etc/netplan/01-netcfg.yaml`**:
```yaml
network:
  version: 2
  # 将 NetworkManager 设置为默认的渲染器
  renderer: NetworkManager
```
<iframe src="https://github-production-user-asset-6210df.s3.amazonaws.com/11393164/351177226-4bea02c9-6d54-4cd6-97ed-dff14340982c.mp4?X-Amz-Algorithm=AWS4-HMAC-SHA256&X-Amz-Credential=AKIAVCODYLSA53PQK4ZA%2F20250924%2Fus-east-1%2Fs3%2Faws4_request&X-Amz-Date=20250924T054437Z&X-Amz-Expires=300&X-Amz-Signature=853ed68824990983b28aea11af7c31078a3475aeb8a8f08420f78fc6194801e9&X-Amz-SignedHeaders=host" scrolling="no" border="0" frameborder="no" framespacing="0" allowfullscreen="true"></iframe>

    """,
    unsafe_allow_html=True,
)
