import { InterruptionModeAndroid, InterruptionModeIOS } from 'expo-av';

export default {
  options: {
    staysActiveInBackground: false,
    allowsRecordingIOS: false,
    playsInSilentModeIOS: true,
    interruptionModeIOS: InterruptionModeIOS.DoNotMix,
    interruptionModeAndroid: InterruptionModeAndroid.DoNotMix,
    playThroughEarpieceAndroid: false,
    shouldDuckAndroid: false,
  }
}
