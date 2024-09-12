FROM node:18-alpine AS builder
WORKDIR /app
COPY ./realworld/package*.json .
RUN npm ci
COPY ./realworld .
RUN npm run build
RUN npm prune --production

FROM node:18-alpine
WORKDIR /app
COPY --from=builder /app/build build/
COPY --from=builder /app/node_modules node_modules/
COPY realworld/package.json .
EXPOSE 3000
ENV NODE_ENV=production
RUN apk add --no-cache bash
CMD [ "node", "build" ]