import React, { useState, useEffect } from 'react';
import { ChakraProvider, Box, Grid, theme } from '@chakra-ui/react';
import { ColorModeSwitcher } from './ColorModeSwitcher';
import Result from './pages/Result';
import Predict from './pages/Predict';
import { useLocalStorage } from './hooks';
import { v4 as uuidv4 } from 'uuid';
import { get } from './api';

function App() {
  const path = window.location.pathname;
  let Page = null;
  if (path.startsWith('/results')) {
    Page = Result;
  } else {
    Page = Predict;
  }
  const [userId, setUserId] = useLocalStorage('oracle:userId', () => uuidv4());
  const [user, setUser] = useState(null);
  useEffect(() => {
    if (userId) {
      get(`users/${userId}`).then(user => setUser(user));
    }
  }, [userId]);
  return (
    <ChakraProvider theme={theme}>
      <Box textAlign="center" fontSize="xl">
        <Grid minH="100vh" p={2}>
          <ColorModeSwitcher justifySelf="flex-end" />
          <Page userId={userId} setUserId={setUserId} user={user} />
        </Grid>
      </Box>
    </ChakraProvider>
  );
}

export default App;
