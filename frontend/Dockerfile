FROM node:20-alpine

WORKDIR /app

COPY package*.json ./
RUN npm config set registry https://registry.npmjs.org/ \
    && npm config set fetch-retries 5 \
    && npm config set fetch-retry-mintimeout 20000 \
    && npm config set fetch-retry-maxtimeout 120000 \
    && npm install

COPY . .

ARG NEXT_PUBLIC_API_URL
ARG NEXT_PUBLIC_API_USERNAME
ARG NEXT_PUBLIC_API_PASSWORD

ENV NEXT_PUBLIC_API_URL=$NEXT_PUBLIC_API_URL
ENV NEXT_PUBLIC_API_USERNAME=$NEXT_PUBLIC_API_USERNAME
ENV NEXT_PUBLIC_API_PASSWORD=$NEXT_PUBLIC_API_PASSWORD

RUN npm run build

EXPOSE 3000

CMD ["npm", "start"]