# Front-end
Front-end built with Typescript, NodeJS, React Native and Expo.

## Install dependencies
First install dependencies with `npm`:
```bash
npm install
```

## Application
To run application with `expo`:
```bash
npm run start
```

To open the application on your mobile phone just scan the QR Code printed on the terminal. For web access: [http://localhost:19000/](http://localhost:19000/).


## WSL2
For WSL2 users that needs to connect application with expo via mobile phone, is necessary to set an envinroment variable `REACT_NATIVE_PACKAGER_HOSTNAME` for expo to start with an IP accessible for your mobile phone in the same network. But, before that you need is just follow [this steps](https://medium.com/codemonday/access-wsl-localhost-from-lan-for-mobile-testing-8635697f008). Note that you need to do it 2 time, first for port `19000` and second for port `8000`.  

Then, change the IP on [package.json](./package.json) adding the output from `ipconfig` IPV4 in the script `start:bridge`, save, then run:
```bash
npm run start:bridge
```

Note that is necessary to export the variable `API_URL` or [change directly in line 2](./constants/Api.ts) with the IPV4 for access from your mobile phone, e.g. `API_URL=http://192.168.X.XX:8000`, it will ensure that you can call the API.
