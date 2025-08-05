# --- Build Stage ---
FROM node:18-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# --- Production Stage ---
FROM node:18-alpine

# Install serve globally for serving static files
RUN npm install -g serve

# Copy the built React app
COPY --from=builder /app/build /app

WORKDIR /app

# Expose port (Railway will set PORT env var)
EXPOSE 3000

# Serve the app (serve automatically reads PORT env var)
CMD ["serve", "-s", "."] 