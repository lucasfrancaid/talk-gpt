import React, { useState, useEffect } from 'react';
import { View, StyleSheet } from 'react-native';
import { AVPlaybackStatusSuccess, Audio } from 'expo-av';
import { Sound, SoundObject } from 'expo-av/build/Audio';
import { FontAwesome5 } from '@expo/vector-icons';
import AudioMode from '../constants/AudioMode';

export interface IAudioMessage {
  content?: string
  role?: string
}

export interface IAudioProps {
  audio: IAudioMessage
  autoPlay: any
}

export default function AudioMessage({ audio, autoPlay }: IAudioProps) {
  if (!audio.content) {
    return <></>
  }

  const [sound, setSound] = useState<Sound>()
  const [status, setStatus] = useState<AVPlaybackStatusSuccess>()
  const [isPlaying, setIsPlaying] = useState<boolean>(false)
  const [isPaused, setIsPaused] = useState<boolean>(false)

  async function getAndSetStatus() {
    let status = await sound?.getStatusAsync()
    status?.isLoaded ? setStatus(status) : setStatus(undefined)
  }

  async function playSound() {
    if (!audio.content) {
      throw new Error('Something wrong with audio content')
    }
    const result: SoundObject = await Audio.Sound.createAsync({ uri: audio.content });
    setSound(result.sound);
    setIsPlaying(true)
    if (result.sound) {
      await result.sound.setPositionAsync(0)
      await result.sound.playAsync();
      await getAndSetStatus()
    }
  }

  async function stopSound() {
    sound?.stopAsync();
    setStatus(undefined)
    setIsPaused(false)
    setIsPlaying(false)
  }

  async function pauseSound() {
    sound?.pauseAsync()
    await getAndSetStatus()
    setIsPaused(true)
    setIsPlaying(false)
  }

  async function continueSound() {
    if (status) {
      sound?.playFromPositionAsync(status.positionMillis)
      setIsPaused(false)
      setIsPlaying(true)
    }
  }

  useEffect(() => {
    Audio.requestPermissionsAsync().then(({ granted }) => {
      if (granted) {
        Audio.setAudioModeAsync(AudioMode.options)
      }
    })
    if (autoPlay && audio.role === 'assistant') {
      playSound().then(() => stopSound())
    }
  }, [])

  useEffect(() => {
    return sound
      ? () => {
        sound.unloadAsync();
      }
      : undefined;
  }, [sound]);

  return (
    <View style={[styles.container, audio.role === 'user' && styles.rootContainer]}>
      {isPaused ? (
        <FontAwesome5
          name='play-circle'
          size={styles.icon.size}
          color={styles.icon.color}
          onPress={continueSound}
        />
      ) : isPlaying ? (
        <FontAwesome5
          name='pause-circle'
          size={styles.icon.size}
          color={styles.icon.color}
          onPress={pauseSound}
        />
      ) : (
        <FontAwesome5
          name='play-circle'
          size={styles.icon.size}
          color={styles.icon.color}
          onPress={playSound}
        />
      )}
      <FontAwesome5
        name='stop-circle'
        size={styles.icon.size}
        color={styles.icon.color}
        onPress={stopSound}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: 'row',
    justifyContent: 'center',
    backgroundColor: '#333333',
    borderRadius: 20,
    paddingTop: 10,
  },
  rootContainer: {
    backgroundColor: '#0084ff'
  },
  icon: {
    color: 'white',
    size: 24,
  },
  button: {
    width: 94,
    height: 94,
    borderRadius: 47,
    backgroundColor: '#b3b3b3',
    marginLeft: 10,
  },
  recording: {
    backgroundColor: '#1db954'
  }
});
