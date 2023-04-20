FROM node:19-alpine

RUN npm install -g pnpm

WORKDIR /app
COPY package.json pnpm-lock.yaml ./
RUN pnpm install --frozen-lockfile

COPY . .
RUN pnpm build


EXPOSE 9009
CMD ["node", "build"]
# CMD ["pnpm", "run", "dev", '--', "--port", "9009"]