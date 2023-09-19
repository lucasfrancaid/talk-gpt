import * as FileSystem from 'expo-file-system';
import { Platform } from 'react-native';
import uuid from 'react-native-uuid'

import Api from '../constants/Api';
import { IMessage } from 'react-native-gifted-chat';
import { IChatMessage } from '../app';


export async function ConvertTextToSpeech(message: string): Promise<any> {
  const result = await fetch(`${Api.url}/chat/text-to-speech`, {
    method: 'POST',
    headers: Api.baseHeaders,
    body: JSON.stringify({ content: message })
  })
    .then((response) => response.blob())
    .then((body) => {
      if (!body) {
        return new Error("Error texting to speech!")
      }
      if (Platform.OS !== 'web') {
        const fr = new FileReader()
        const fileUri = `${FileSystem.documentDirectory}${uuid.v4()}.mp3`
        fr.onload = async (readerEvent: ProgressEvent<FileReader>) => {
          if (readerEvent.target && readerEvent.target.result)
            await FileSystem.writeAsStringAsync(
              fileUri,
              String(readerEvent.target?.result)?.split(',')[1],
              { encoding: FileSystem.EncodingType.Base64 }
            )
        }
        fr.readAsDataURL(body)
        return fileUri
      }
      return URL.createObjectURL(body)
    })
    .catch((err) => console.error(err));
  return result
}

export async function ConvertSpeechToText(uri: string): Promise<any> {
  const formData = new FormData()

  if (Platform.OS === 'web') {
    const blob = await fetch(uri).then(result => result.blob())
    formData.append('file', blob)
    formData.append('type', 'audio/webv')
  } else {
    const filename = uri.split('/').slice(-1)[0]
    const fileType = uri.split('.').slice(-1)[0]
    const file = {
      uri: uri,
      name: filename,
      type: `audio/x-${fileType}`,
    }
    formData.append('file', JSON.parse(JSON.stringify(file)))
  }

  const result = await fetch(`${Api.url}/chat/speech-to-text`, {
    method: 'POST',
    headers: {
      Accept: 'application/json',
    },
    body: formData,
  })
    .then((response) => response.json())
    .then((json) => {
      if (json.detail) {
        throw new Error(`Unexpected error calling API: ${JSON.stringify(json)}`)
      }
      return json.content
    })
    .catch((err) => {
      console.error(err)
      return 'Failed to load transcripted data'
    });

  return result
}

export async function GetChatHistory(): Promise<IMessage[]> {
  const result = await fetch(`${Api.url}/chat/message/history`, {
    method: 'GET',
    headers: Api.baseHeaders,
  })
    .then((response) => response.json())
    .then((json) => {
      let msgs = json.map((item: IChatMessage) => {
        return {
          _id: String(uuid.v4()),
          text: item.content,
          createdAt: new Date(),
          user: item.role === "user" ? Api.rootUser : Api.systemUser,
        }
      })
      return msgs
    })
    .catch((err) => console.error(err));
  return result
}
