# 排查 HTTPS 连接问题

## 当前状态
- ✅ Nginx 配置测试通过
- ❌ 浏览器访问 `https://www.tangxinhao.online` 显示 `ERR_CONNECTION_REFUSED`

## 可能的原因

### 1. 443 端口未开放（最可能）
- 阿里云安全组未开放 443 端口
- 服务器防火墙未开放 443 端口

### 2. Nginx 容器未正常启动
- 容器可能启动失败
- 证书文件路径在容器内找不到

### 3. 域名解析问题
- 域名可能未正确解析到服务器 IP

## 排查步骤

### 步骤 1：检查 Nginx 容器状态

```bash
docker ps | grep nginx
```

应该看到 `hsk-nginx` 容器在运行。

如果没看到，检查容器日志：
```bash
docker logs hsk-nginx --tail 50
```

### 步骤 2：检查 443 端口是否监听

```bash
netstat -tlnp | grep 443
```

或者：
```bash
ss -tlnp | grep 443
```

应该看到类似：
```
tcp  0  0  0.0.0.0:443  LISTEN  xxx/nginx
```

如果没有输出，说明 443 端口没有监听。

### 步骤 3：检查证书文件在容器内是否存在

```bash
docker exec hsk-nginx ls -la /etc/nginx/ssl/tangxinhao.online/
```

应该看到 `cert.pem` 和 `cert.key`。

如果提示 "No such file or directory"，说明证书文件路径映射有问题。

### 步骤 4：检查阿里云安全组（重要！）

1. 登录 [阿里云控制台](https://ecs.console.aliyun.com)
2. 进入：**云服务器 ECS** → **实例**
3. 找到你的服务器实例
4. 点击 **安全组** → **配置规则**
5. 检查 **入方向规则** 中是否有 **443 端口**
   - 如果没有，点击 **添加安全组规则**
   - 端口范围：`443/443`
   - 授权对象：`0.0.0.0/0`
   - 协议类型：`TCP`
   - 描述：`HTTPS`

### 步骤 5：检查服务器防火墙

```bash
# 如果使用 ufw
ufw status
ufw allow 443/tcp

# 如果使用 firewalld
firewall-cmd --list-ports
firewall-cmd --permanent --add-port=443/tcp
firewall-cmd --reload

# 如果使用 iptables
iptables -L -n | grep 443
```

## 快速检查命令

```bash
# 1. 检查容器状态
docker ps | grep nginx

# 2. 检查 443 端口
netstat -tlnp | grep 443

# 3. 检查证书文件
docker exec hsk-nginx ls -la /etc/nginx/ssl/tangxinhao.online/

# 4. 查看 Nginx 日志
docker logs hsk-nginx --tail 50
```
