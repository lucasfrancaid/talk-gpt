export default {
  url: process.env.API_URL || 'http://localhost:3333',
  baseHeaders: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  },
  rootUser: {
    _id: 1,
    name: 'Lucas',
    avatar: 'https://avatars.githubusercontent.com/u/54768967?v=4',
  },
  systemUser: {
    _id: 2,
    name: 'Kara',
    avatar: 'https://avatars.githubusercontent.com/u/82469147?v=4',
  }
};
