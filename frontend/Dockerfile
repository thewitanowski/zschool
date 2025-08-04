# --- Build Stage ---
# This stage builds the React application
FROM node:18-alpine AS builder

# Set the working directory inside the container
WORKDIR /app

# Copy package.json and package-lock.json to the workdir
# This leverages Docker's layer caching. These files don't change often.
COPY package*.json ./

# Install dependencies cleanly and reproducibly from the lock file
RUN npm ci

# Copy the rest of the application source code (public, src, etc.)
COPY . .

# Build the React app for production. The output will be in /app/build
RUN npm run build


# --- Production Stage ---
# This stage serves the built static files using nginx
FROM nginx:1.25-alpine

# Copy the optimized production build from the 'builder' stage
# into the nginx public html directory.
COPY --from=builder /app/build /usr/share/nginx/html

# Expose port 80 for the nginx server
EXPOSE 80

# Start nginx in the foreground when the container launches
CMD ["nginx", "-g", "daemon off;"] 