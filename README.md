# 🎓 Welcome!

In this course we will be working with virtual servers based on Ubuntu 24.04. On these servers, we will run Jupyter Lab to enable easy access to servers' resources using the web interface you should already be familiarized with.  Inside Jupyter, we will run our NS-3 simulations. 

There are currently 13 virtual servers with private addresses in range **10.100.0.41-53/23**. These are accessible via our gateway that has a VSB-connected address **158.196.244.134**.

Access your resources easily using the following mappings. This guide will help you connect to Jupyter, SSH, and XSession services hosted on our server.

---

## 🔐 Connecting via SSH

First, you will need to connect to your server using SSH. To connect, use the following mapping:

```
158.196.244.134:<last-octet-of-server-ip>22
```

### Example:

If the server IP is `10.100.0.41`, the SSH command becomes:

```
ssh student@158.196.244.134 -p 4122
```

---

## 🚀 Running Jupyter Lab

To run Jupyter Lab on the server, follow these steps:

1. ssh student@158.196.244.134 -p <last-octet-of-server-ip>22
2. source venv-ns3-2025/bin/activate
3. jupyter lab --ip 0.0.0.0 --port 8443

---

## 🌐 Accessing Jupyter Notebook

You can access Jupyter Notebook using the following URL:

```
http://158.196.244.134:<last-octet-of-server-ip>443
```

### Example:
If the server IP is `10.100.0.41`, the URL becomes:

```
http://158.196.244.134:41443
```

---

## 🖥️ Using Xpra

For Xpra, use the following mapping:

`158.196.244.134:<last-octet-of-server-ip>100`

### Example:

If the server IP is `10.100.0.41`, the Xpra connection becomes:

`xpra attach ssh:user@158.196.244.134 -p 41100`

## 🛠️ Commands

Here, you can find the commands to set up and connect to the services. This section will be updated as necessary!

---

### 🤔 Need Help?
If you encounter any issues or have questions, feel free to reach out to your instructor or system administrator.

Happy Learning! 🚀