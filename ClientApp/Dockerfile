# Stage 1: Compile and Build angular codebase
# Stage 2: Host the application using Nginx

# Use official node image as the base image
FROM node:latest as angularbuild
# Set the working directory
WORKDIR /src/app
# Copy package.json and package-lock.json
COPY package*.json .

# Install all the dependencies
RUN npm install
RUN npm install -g @angular/cli
# Copy the rest of your app's source code
COPY . .
FROM angularbuild as final
EXPOSE 4200
# ENTRYPOINT  ["sleep", "infinity"]
CMD ["ng", "serve", "--host", "0.0.0.0", "--configuration", "development"]
# Build the angular app
# ENTRYPOINT ["npm", "start", "--", "--host", "0.0.0.0", "--poll", "500"]
# # Stage 2: Host the application using Nginx
# FROM nginx:latest
# # Copy the dist folder to the nginx web root
# COPY --from=angularbuild /app/dist /usr/share/nginx/html
# # Copy the Nginx configuration
# COPY nginx.conf /etc/nginx/conf.d/default.conf
# # Start Nginx
# CMD ["nginx", "-g", "daemon off;"]

