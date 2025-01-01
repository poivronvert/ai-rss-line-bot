# Install dependencies only when needed
ARG NODE_VERSION=20
FROM --platform=linux/amd64 node:${NODE_VERSION} AS deps
RUN apt-get update && apt-get install -y libc6 && rm -rf /var/lib/apt/lists/*
WORKDIR /app
COPY package.json ./
RUN yarn install --frozen-lockfile

# Rebuild the source code only when needed
FROM --platform=linux/amd64 node:${NODE_VERSION} AS builder
WORKDIR /app
COPY . .
COPY --from=deps /app/node_modules ./node_modules
RUN yarn build

# Production image, copy all the files and run next
FROM --platform=linux/amd64 node:${NODE_VERSION} AS runner
WORKDIR /app
COPY --from=builder /app ./
COPY --from=deps /app/node_modules ./node_modules
ENV NEXT_PUBLIC_BACKEND_URL=YOUR_URL
EXPOSE 8080
ENV PORT=8080
CMD ["yarn", "start"]