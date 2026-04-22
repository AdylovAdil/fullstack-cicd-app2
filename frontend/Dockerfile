FROM node:18

WORKDIR /app

COPY package*.json ./
RUN npm install

COPY . .

RUN npm run build

RUN npm install -g serve

CMD ["sh", "-c", "npx serve -s dist -l ${PORT:-3000}"]