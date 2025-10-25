FROM node:14.16.0

WORKDIR /linafe
# COPY package*.json ./

# Instala dependencias (opcional en dev si usas bind mount + volumen node_modules)
# Para prod deja esto activo para que la imagen tenga todo:
# RUN npm ci --only=production
# RUN npm ci

COPY . .

EXPOSE 3001

# En dev se sobreescribe por compose (npm run dev)
# En prod (fe_prod) usamos "npm run start" desde compose