import * as React from 'react';
import { View, StyleSheet, Button } from 'react-native';
import * as Speech from 'expo-speech';
import { IAudioMessage } from './Audio';


export default function TextToSpeech(audio: IAudioMessage) {
  if (!audio.content) {
    return <></>
  }

  const speak = () => {
    const options = {
      language: 'en',
      pitch: 1.0,
      rate: 0.7,
    }
    Speech.speak(String(audio.content), options);
  };

  const stop = () => {
    Speech.stop()
  }

  const pause = () => {
    Speech.pause()
  }

  const resume = () => {
    Speech.resume()
  }

  return (
    <View style={styles.container}>
      <Button title="Play" onPress={speak} />
      <Button title="Stop" onPress={stop} />
      <Button title="Pause" onPress={pause} />
      <Button title="Resume" onPress={resume} />
    </View>
  );
}

const styles = StyleSheet.create({
  container: {},
});
