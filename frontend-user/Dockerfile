# 构建阶段
# 使用较新的 Node 22 版本，并配合国内 npm 镜像，加快依赖安装
FROM node:22-alpine as build

WORKDIR /app

# 复制package文件
COPY package*.json ./

# 使用国内 npm 镜像并安装依赖
RUN npm config set registry https://registry.npmmirror.com \
    && npm ci --only=production=false

# 复制源代码
COPY . .

# 设置API地址环境变量（生产环境使用正式域名）
ARG VITE_API_BASE_URL=https://tangxinhao.online
ENV VITE_API_BASE_URL=$VITE_API_BASE_URL

# 构建应用（限制 Node.js 内存使用，避免 OOM）
ENV NODE_OPTIONS="--max-old-space-size=1024"
RUN npm run build

# 生产阶段
FROM nginx:alpine

# 复制构建产物
COPY --from=build /app/dist /usr/share/nginx/html

# 复制nginx配置
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
