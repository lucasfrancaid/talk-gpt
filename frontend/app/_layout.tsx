import React, { useEffect, useState } from 'react';
import { Switch, useColorScheme } from 'react-native';

import { DarkTheme, DefaultTheme, ThemeProvider } from '@react-navigation/native';
import { SplashScreen, Stack } from 'expo-router';
import { useFonts } from 'expo-font';
import FontAwesome from '@expo/vector-icons/FontAwesome';

export {
  ErrorBoundary,
} from 'expo-router';

// export const unstable_settings = {
//   initialRouteName: 'index.tsx',
// };

export default function RootLayout() {
  const [loaded, error] = useFonts({
    SpaceMono: require('../assets/fonts/SpaceMono-Regular.ttf'),
    ...FontAwesome.font,
  });

  // Expo Router uses Error Boundaries to catch errors in the navigation tree.
  useEffect(() => {
    if (error) throw error;
  }, [error]);

  return (
    <>
      {/* Keep the splash screen open until the assets have loaded. In the future, we should just support async font loading with a native version of font-display. */}
      {!loaded && <SplashScreen />}
      {loaded && <RootLayoutNav />}
    </>
  );
}

function RootLayoutNav() {
  // const [autoPlay, setAutoPlay] = useState<boolean>(false)

  const colorScheme = useColorScheme();

  // const Header = () => {
  //   return (
  //     <Switch
  //       trackColor={{ false: '#767577', true: '#81b0ff' }}
  //       thumbColor={autoPlay ? '#f5dd4b' : '#f4f3f4'}
  //       onValueChange={() => setAutoPlay(previousState => !previousState)}
  //       value={autoPlay}
  //     />
  //   )
  // }

  return (
    <>
      <ThemeProvider value={colorScheme === 'dark' ? DarkTheme : DefaultTheme}>
        <Stack
          screenOptions={{
            title: 'Speak GPT',
            headerShown: false,
            // headerTitle: () => <Header />
          }} />
      </ThemeProvider>
    </>
  );
}
