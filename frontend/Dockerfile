# --- Stage 1: Build ---
# Use Node.js image to build the app
FROM node:20-alpine AS builder

# Set working directory
WORKDIR /app

# Copy package files and install dependencies
COPY package*.json ./
RUN npm install

# Copy the rest of the code
COPY . .

# Build the app
RUN npm run build

# --- Stage 2: Production ---
# Use lightweight Nginx to serve static files
FROM nginx:stable-alpine

# Copy built files from builder stage
COPY --from=builder /app/dist /usr/share/nginx/html

# Copy Nginx configuration
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expose port 80
EXPOSE 80

# Nginx will start automatically
