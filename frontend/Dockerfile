FROM node:20-alpine AS build

WORKDIR /app

COPY package.json ./
RUN npm install

COPY . .

ARG VITE_API_URL
ARG VITE_STUDENT_NAME
ARG VITE_STUDENT_ID

ENV VITE_API_URL=$VITE_API_URL
ENV VITE_STUDENT_NAME=$VITE_STUDENT_NAME
ENV VITE_STUDENT_ID=$VITE_STUDENT_ID

RUN npm run build

FROM nginx:1.27-alpine

COPY --from=build /app/dist /usr/share/nginx/html

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
