import React from 'react';
import { ChakraProvider, Box, Grid, theme } from '@chakra-ui/react';
import { ColorModeSwitcher } from './ColorModeSwitcher';
import Result from './pages/Result';
import Predict from './pages/Predict';
import { useLocalStorage } from './hooks';
import { v4 as uuidv4 } from 'uuid';

function App() {
  const path = window.location.pathname;
  let Page = null;
  if (path.startsWith('/results')) {
    Page = Result;
  } else {
    Page = Predict;
  }
  const [userId] = useLocalStorage('oracle:userId', () => uuidv4());
  return (
    <ChakraProvider theme={theme}>
      <Box textAlign="center" fontSize="xl">
        <Grid minH="100vh" p={2}>
          <ColorModeSwitcher justifySelf="flex-end" />
          <Page userId={userId} />
        </Grid>
      </Box>
    </ChakraProvider>
  );
}

export default App;
