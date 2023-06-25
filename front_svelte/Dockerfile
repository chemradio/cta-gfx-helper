FROM node:19-alpine AS builder
ENV NODE_ENV=production
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm install --include=dev
COPY . .
RUN npm run build
RUN npm install --include=dev

# FROM node:19-alpine
# USER node:node
# WORKDIR /app
# COPY --from=builder --chown=node:node /app/build ./build
# COPY --from=builder --chown=node:node /app/node_modules ./node_modules
# COPY --chown=node:node package.json .

ENV HOST=0.0.0.0
ENV PORT=80
# ENV PROTOCOL_HEADER="x-forwarded-proto"
# ENV HOST_HEADER="x-forwarded-host"
# ENV ORIGIN="http://localhost:9009"

# EXPOSE 9009

CMD ["npm","run", "preview", "--", "--host", "0.0.0.0", "--port", "80"]

# ENTRYPOINT npm run dev
# CMD ["node", "build"]