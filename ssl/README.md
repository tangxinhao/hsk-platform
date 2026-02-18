# SSL 证书目录

## 目录结构

```
ssl/
└── tangxinhao.online/
    ├── cert.pem    # 证书文件（从阿里云下载的 .pem 文件）
    └── cert.key    # 私钥文件（从阿里云下载的 .key 文件）
```

## 如何获取证书文件

1. 登录 [阿里云控制台](https://ecs.console.aliyun.com)
2. 进入：**产品与服务** → **数字证书管理服务** → **SSL证书管理**
3. 找到证书 `cert-wmwmfb`（www.tangxinhao.online）
4. 点击 **下载** → 选择 **Nginx** 格式
5. 解压后得到两个文件，重命名为：
   - `cert.pem`（原证书文件）
   - `cert.key`（原私钥文件）
6. 将这两个文件上传到 `ssl/tangxinhao.online/` 目录

## 注意事项

- 证书文件必须命名为 `cert.pem` 和 `cert.key`
- 确保文件权限正确（建议 644 或 600）
- 证书有效期至 2026-05-11，到期前需要续期
