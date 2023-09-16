const fs = require('fs');
const openai = require('openai');
const speech = require('@google-cloud/speech');
const gtts = require('gtts');
const { v4: uuidv4 } = require('uuid');
const { promisify } = require('util');

const readFileAsync = promisify(fs.readFile);
const writeFileAsync = promisify(fs.writeFile);

const GPT_MODEL = "gpt-3.5-turbo";
const VOICE_FROM_FILE = "";
const VOICE_FILE = "";
const VOICE_FILE_EXT = "";

openai.apiKey = process.env.OPENAI_KEY;
openai.organization = "";

const client = new speech.SpeechClient();

let _messages = [];

function playContent(content) {
  const tts = new gtts(content, 'en');
  const audioFileName = `audio_${uuidv4()}.mp3`;

  tts.save(audioFileName, function (err, result) {
    if (err) {
      console.error('Error saving audio:', err);
      return;
    }

    const filePath = `./${audioFileName}`;
    const audioFile = fs.readFileSync(filePath);

    fs.writeFileSync('audio.wav', audioFile);
    fs.unlinkSync(filePath);

    const file = fs.readFileSync('audio.wav');
    const audioBytes = file.toString('base64');

    const audio = {
      content: audioBytes,
    };
    const config = {
      encoding: 'LINEAR16',
      sampleRateHertz: 16000,
      languageCode: 'en-US',
    };
    const request = {
      audio: audio,
      config: config,
    };

    client
      .recognize(request)
      .then((data) => {
        const response = data[0];
        const transcription = response.results
          .map((result) => result.alternatives[0].transcript)
          .join('\n');
        console.log('\nRecorded:', transcription);
        const isvalidRecord = input('\n--> Recorded message is valid? (y/n): ');
        if (isvalidRecord.toLowerCase() in ['n', 'no', 'not']) {
          return playContent();
        }
        return transcription;
      })
      .catch((err) => {
        console.error('Error recognizing speech:', err);
      });
  });
}

async function getContent() {
  let exceptionRetries = 0;
  while (true) {
    try {
      await promisify(fs.access)(VOICE_FROM_FILE, fs.constants.F_OK);
      const fileData = await readFileAsync(VOICE_FROM_FILE);
      await writeFileAsync(VOICE_FILE, fileData);
      await promisify(fs.unlink)(VOICE_FROM_FILE);

      const audio = await readFileAsync(VOICE_FILE);
      const audioBytes = audio.toString('base64');

      const request = {
        audio: {
          content: audioBytes,
        },
        config: {
          encoding: 'LINEAR16',
          sampleRateHertz: 16000,
          languageCode: 'en-US',
        },
      };

      const [response] = await client.recognize(request);
      const transcription = response.results
        .map((result) => result.alternatives[0].transcript)
        .join('\n');

      console.log(`\nRecorded: ${transcription}`);
      const isValidRecord = input('\n--> Recorded message is valid? (y/n): ');
      if (isValidRecord.toLowerCase() in ['n', 'no', 'not']) {
        exceptionRetries = 0;
        continue;
      }

      return transcription;
    } catch (err) {
      if (err.code === 'ENOENT') {
        if (exceptionRetries === 108) {
          process.exit();
        }
        console.log('\n--> Record an audio in the client to send a message');
        await promisify(setTimeout)(5000);
        exceptionRetries += 1;
        continue;
      }

      console.error('Error:', err);
      break;
    }
  }
}

function inputContent(voiceMode) {
  if (!voiceMode) {
    const content = input('\n--> Type here: ');
    return content;
  }

  const content = getContent();
  console.log(`\nUser: ${content}\n`);
  return content;
}

function generateMessage(role, content) {
  return {
    role: role,
    content: content,
  };
}

function appendAIMessage(message) {
  _messages.push(generateMessage(message.role, message.content));
}

async function chatCompletionProcess() {
  const chatCompletion = await openai.ChatCompletion.create({
    model: GPT_MODEL,
    messages: _messages,
  });
  appendAIMessage(chatCompletion.choices[0].message);
}

function printLastMessage(playAudio = false) {
  const lastMessage = _messages[_messages.length - 1];
  console.log(`${lastMessage.role.charAt(0).toUpperCase() + lastMessage.role.slice(1)}: ${lastMessage.content}`);
  if (playAudio) {
    console.log('\n');
    playContent(lastMessage.content);
  }
}

async function main(voiceMode = false) {
  console.log('--> Welcome to SpeakGPT, focused to improve your English. \n');
  console.log('Present yourself to AI English Teacher. \n');

  const firstContent = inputContent({ voiceMode });

  const extendedContext = !voiceMode
    ? ''
    : "Don't reply with prompts, each reply must be a message and this message will be transcribed to " +
      'audio, so return the message formatted to it. Sometimes I will ask for a mock conversation about ' +
      'specific topics, so you need to handle with it just through messages and not returning prompts.';

  _messages.push(
    generateMessage('system', `You are an AI English Teacher focused in conversational study with British accent. ` +
      `This chat must look like a real conversation between student and teacher. ${extendedContext}` +
      `Another thing you must be is, when I make some mistake in my sentence you need to correct me ` +
      `saying what I did wrong and explaining the correct way. \n\n`)
  );
  _messages.push(generateMessage('user', firstContent));
  printLastMessage(false);

  await chatCompletionProcess();
  while (true) {
    printLastMessage(voiceMode);
    const content = inputContent({ voiceMode });
    _messages.push(generateMessage('user', content));

    try {
      console.log('\n--> Processing message...');
      await chatCompletionProcess();
    } catch (err) {
      console.error('Error:', err);
      if (err.shouldRetry) {
        console.log('\n--> Retrying based on OpenAI recommendation...');
        continue;
      }

      console.log('\n--> Sleeping for 5 seconds to retry');
      await promisify(setTimeout)(5000);
      console.log('\n--> Retrying by myself...');
    }
  }
}

const args = process.argv.slice(2);
const isVoiceMode = args.includes('-c') && args[args.indexOf('-c') + 1] === 'voice';
main(isVoiceMode);
