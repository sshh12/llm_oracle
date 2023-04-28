import React from 'react';
import { ChakraProvider, Box, Grid, theme } from '@chakra-ui/react';
import { ColorModeSwitcher } from './ColorModeSwitcher';
import Result from './pages/Result';
import Predict from './pages/Predict';

function App() {
  const path = window.location.pathname;
  let Page = null;
  if (path.startsWith('/results')) {
    Page = Result;
  } else {
    Page = Predict;
  }
  return (
    <ChakraProvider theme={theme}>
      <Box textAlign="center" fontSize="xl">
        <Grid minH="100vh" p={2}>
          <ColorModeSwitcher justifySelf="flex-end" />
          <Page />
        </Grid>
      </Box>
    </ChakraProvider>
  );
}

export default App;
