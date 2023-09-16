import React, { useState, useCallback, useEffect } from 'react'
import { useColorScheme, StyleSheet, Platform, Pressable, Vibration, Switch, ActivityIndicator } from 'react-native';
import { GiftedChat, IMessage, Bubble, InputToolbar, Composer, Send } from 'react-native-gifted-chat'
import { Audio } from 'expo-av';
import uuid from 'react-native-uuid'
import { FontAwesome5 } from '@expo/vector-icons';

import { Text, View } from '../components/Themed';
import AudioMessage from '../components/Audio';
import Api from '../constants/Api';
import AudioMode from '../constants/AudioMode';
import { GetChatHistory, ConvertTextToSpeech, ConvertSpeechToText } from '../services/Chat';

export interface IChatMessage {
  role: string
  content: string
}

export interface IChatProps {
  autoPlay: boolean
}

export default function Chat() {
  const [autoPlay, setAutoPlay] = useState<boolean>(false)
  const [isTyping, setIsTyping] = useState<boolean>(false)
  const [messages, setMessages] = useState<IMessage[]>([])
  const [recording, setRecording] = useState<Audio.Recording>()
  const [isLoadingRecorded, setIsLoadingRecorded] = useState<boolean>(false)
  const [recordFileUri, setRecordFileUri] = useState<string>()
  const [recordedAudioText, setRecordedAudioText] = useState<string>()
  const [onLongPress, setOnLongPress] = useState<boolean>(false)

  useEffect(() => {
    Audio.requestPermissionsAsync().then(({ granted }) => {
      if (granted) {
        Audio.setAudioModeAsync(AudioMode.options)
      }
    })
  }, [])

  useEffect(() => {
    const fetchHistory = async () => {
      const history = await GetChatHistory()
      return history;
    }
    fetchHistory().then((history) => setMessages(history.reverse()))
  }, [])

  const onSend = useCallback((newMessages: IMessage[] = []) => {
    newMessages.map((item) => item._id = String(uuid.v4()))
    setMessages(previousMessages => GiftedChat.append(previousMessages, newMessages))

    const message = {
      role: 'user',
      content: newMessages.slice(-1)[0].text,
    }

    setIsTyping(true)

    fetch(`${Api.url}/chat/message`, {
      method: 'POST',
      headers: Api.baseHeaders,
      body: JSON.stringify(message),
    })
      .then((response) => response.json())
      .then(async (json) => {
        let aiMessage: IMessage = {
          _id: String(uuid.v4()),
          text: json.content,
          createdAt: new Date(),
          user: Api.systemUser,
          audio: await ConvertTextToSpeech(json.content),
        }
        messages.push(aiMessage)
        setIsTyping(false)
        setMessages(previousMessages => GiftedChat.append(previousMessages, [aiMessage]))
      })
      .catch((err) => {
        setIsTyping(false)
        console.error(err)
      });
  }, [])

  async function handleRecording() {
    if (recording) {
      return stopRecording()
    }
    return startRecording()
  }

  async function startRecording() {
    await Audio.setAudioModeAsync({ ...AudioMode.options, ...{ allowsRecordingIOS: true } })
    const { granted } = await Audio.requestPermissionsAsync()
    if (!granted) {
      Audio.requestPermissionsAsync().then(({ granted }) => {
        if (!granted) {
          throw new Error("Permission is necessary to record audio")
        }
        Audio.setAudioModeAsync(AudioMode.options)
      })
    }
    if (Platform.OS === 'ios' || Platform.OS === 'android') {
      Vibration.vibrate()
    }
    try {
      const status = await Audio.Recording.createAsync()
      setRecording(status.recording)
    } catch (error) {
      console.error(error)
    }
  }

  async function stopRecording() {
    if (Platform.OS === 'ios' || Platform.OS === 'android') {
      Vibration.vibrate()
    }
    try {
      if (recording) {
        await recording.stopAndUnloadAsync()
        const fileUri = recording.getURI()
        if (fileUri) {
          setOnLongPress(false)
          setRecordFileUri(fileUri)
          setRecording(undefined)
          readRecord(fileUri)
        }
      }
    } catch (error) {
      console.error(error)
    }
    await Audio.setAudioModeAsync(AudioMode.options)
  }

  async function readRecord(uri: string) {
    setIsLoadingRecorded(true)
    if (!uri) {
      throw new Error("Error to try read voice message, audio not found")
    }
    const text = await ConvertSpeechToText(uri)
    setIsLoadingRecorded(false)
    setRecordedAudioText(text)
  }

  async function cancelRecord() {
    setOnLongPress(false)
    setIsLoadingRecorded(false)
    setRecordedAudioText(undefined)
    setRecordFileUri(undefined)
  }

  async function sendRecord() {
    if (!recordFileUri || !recordedAudioText) {
      throw new Error("Error to try send voice message, audio not found")
    }
    const audioText = recordedAudioText
    const fileUri = recordFileUri
    setRecordedAudioText(undefined)
    setRecordFileUri(undefined)
    let voiceMessage: IMessage = {
      _id: String(uuid.v4()),
      text: audioText,
      createdAt: new Date(),
      user: Api.rootUser,
      audio: fileUri,
    }
    onSend([voiceMessage])
  }

  const colorScheme = useColorScheme();

  const Header = () => (
    <View style={styles.navContainer}>
      <Text style={{ marginBottom: '1%', fontSize: 16, marginEnd: '2%' }}>Auto Play</Text>
      <Switch
        trackColor={{ false: '#767577', true: '#81b0ff' }}
        thumbColor={autoPlay ? '#f5dd4b' : '#f4f3f4'}
        ios_backgroundColor="#3e3e3e"
        onValueChange={() => setAutoPlay(previousState => !previousState)}
        value={autoPlay}
        style={styles.nav}
      />
    </View>
  )

  // async function bubbleOnLongPress(props: any): Promise<void> {
  //   console.log(props)
  // }

  return (
    <View style={styles.container}>
      {/* <Text style={styles.title}>SpeakGPT - AI English Teacher</Text> */}
      <Header />
      <GiftedChat
        messages={messages}
        onSend={messages => onSend(messages)}
        user={Api.rootUser}
        showUserAvatar={true}
        scrollToBottom={true}
        isTyping={isTyping}
        renderBubble={props => {
          return (
            <Bubble
              {...props}
              textStyle={{
                left: {
                  color: colorScheme == 'dark' ? '#fff' : '#000'
                }
              }}
              wrapperStyle={{
                left: {
                  backgroundColor: colorScheme == 'dark' ? '#333333' : '#f0f0f0',
                },
              }}
            // onLongPress={props => bubbleOnLongPress(props)}
            />
          );
        }}
        renderInputToolbar={props => {
          return (
            <InputToolbar
              {...props}
              containerStyle={{
                borderRadius: 20,
                marginHorizontal: 5,
                borderColor: colorScheme == 'dark' ? '#fff' : '#000',
                borderWidth: 0.3,
                backgroundColor: colorScheme == 'dark' ? '#000' : '#fff',
              }}
              renderComposer={props1 => (
                <>
                  {recordFileUri && recordedAudioText ? (
                    <Composer
                      {...props1}
                      textInputStyle={{
                        color: colorScheme == 'dark' ? '#fff' : '#000',
                        backgroundColor: '#333333',
                      }}
                      text={recordedAudioText}
                      multiline={true}
                      onTextChanged={text => setRecordedAudioText(text)}  // A way to remove text when record is canceled
                    />
                  ) : (
                    <>
                      <Composer
                        {...props1}
                        textInputStyle={{
                          color: colorScheme == 'dark' ? '#fff' : '#000',
                        }}
                      />
                      {isLoadingRecorded && <ActivityIndicator style={styles.loading} size='large' />}
                    </>
                  )}
                </>
              )}
              renderSend={props2 => (
                <View style={styles.toolbar}>
                  {!recordFileUri && !recordedAudioText &&
                    <Send
                      {...props2}
                      containerStyle={{
                        borderColor: colorScheme == 'dark' ? '#00ffff' : '#000',
                        marginEnd: 5,
                      }}
                    />
                  }
                  {!isLoadingRecorded && recordFileUri ? (
                    <>
                      <View style={styles.recordedMessage}>
                        <FontAwesome5
                          name='trash-alt'
                          size={styles.icon.size}
                          color='#D22B2B'
                          onPress={cancelRecord}
                        />
                      </View>
                      <View style={styles.recordedMessage}>
                        <FontAwesome5
                          name='arrow-alt-circle-right'
                          size={styles.icon.size}
                          color='#0084ff'
                          onPress={sendRecord}
                        />
                      </View>
                    </>
                  ) : !isLoadingRecorded ? (
                    <>
                      <Pressable
                        style={[styles.button, recording && styles.recording]}
                        onPressIn={handleRecording}
                        onLongPress={() => setOnLongPress(true)}
                        onPressOut={() => !onLongPress ? stopRecording() : undefined}
                        delayLongPress={3000}
                        pressRetentionOffset={
                          { bottom: 500, left: 500, right: 500, top: 500 }
                        }
                      >
                        <FontAwesome5
                          name='microphone'
                          size={styles.icon.size}
                          color={styles.icon.color}
                        />
                      </Pressable>
                    </>
                  ) : (<></>)}
                </View>
              )}
            />
          );
        }}
        renderMessageAudio={props3 => (
          <AudioMessage
            {...props3}
            audio={{
              content: props3.currentMessage?.audio,
              role: props3.currentMessage?.user._id === 1 ? 'user' : props3.currentMessage?.user._id === 2 ? 'assistant' : 'system'
            }}
            autoPlay={autoPlay}
          />
        )}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  navContainer: {
    position: 'relative',
    display: 'flex',
    flexDirection: 'row',
    alignItems: 'flex-end',
    justifyContent: 'flex-end',
    height: '10%',
    backgroundColor: '#000',
    padding: 8,
  },
  nav: {
    marginEnd: '3%',
  },
  container: {
    flex: 1,
    paddingBottom: 7,
    paddingTop: 0,
  },
  title: {
    fontSize: 20,
    fontWeight: 'bold',
  },
  toolbar: {
    flexDirection: 'row',
  },
  icon: {
    color: 'white',
    size: 24,
  },
  button: {
    width: 40,
    height: 40,
    borderRadius: 40,
    backgroundColor: '#b3b3b3',
    alignItems: 'center',
    justifyContent: 'center',
    marginRight: 35,
    marginBottom: 7,
  },
  recording: {
    backgroundColor: '#0084ff'
  },
  recordedMessage: {
    backgroundColor: '#333333',
    borderRadius: 20,
    margin: 8,
  },
  loading: {
    marginEnd: '90%',
    marginBottom: '1.5%'
  }
});
