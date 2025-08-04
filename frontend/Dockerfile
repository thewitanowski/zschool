# --- Build Stage ---
# Use an official Node.js runtime as a parent image for the build stage
FROM node:18-alpine AS builder

# Set the working directory in the container
WORKDIR /app

# Copy package.json and package-lock.json from the frontend subdirectory
COPY frontend/package*.json ./

# Install dependencies
# Using 'npm ci' for clean, reproducible installs from package-lock.json
RUN npm ci

# Copy the rest of the frontend application source code into the container
COPY frontend/ .

# Build the React application for production
RUN npm run build


# --- Production Stage ---
# Use a lean nginx image for a small production environment
FROM nginx:1.25-alpine

# Copy the optimized build output from the 'builder' stage to the nginx web root directory
COPY --from=builder /app/build /usr/share/nginx/html

# Expose port 80 to the outside world
EXPOSE 80

# The container will run nginx and serve the static files
CMD ["nginx", "-g", "daemon off;"] 