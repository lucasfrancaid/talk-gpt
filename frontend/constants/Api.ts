export default {
  url: process.env.API_URL || 'http://localhost:8000',
  baseHeaders: {
    Accept: 'application/json',
    'Content-Type': 'application/json',
  },
  rootUser: {
    _id: 1,
    name: 'User',
    avatar: 'https://raw.githubusercontent.com/lucasfrancaid/talk-gpt/main/frontend/assets/images/talk_gpt_white.png',
  },
  systemUser: {
    _id: 2,
    name: 'AI',
    avatar: 'https://raw.githubusercontent.com/lucasfrancaid/talk-gpt/main/frontend/assets/images/talk_gpt_orange.png',
  }
};
