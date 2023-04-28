import React, { useState } from 'react';
import { APP_HOST } from '../api';
import {
  Text,
  Link,
  VStack,
  Stack,
  InputGroup,
  Input,
  IconButton,
  Button,
} from '@chakra-ui/react';
import { SearchIcon, SettingsIcon, ExternalLinkIcon } from '@chakra-ui/icons';

function Predict() {
  const [q, setQ] = useState('');
  return (
    <VStack spacing={7}>
      <Text fontSize={'5rem'}>🔮</Text>
      <Stack spacing={1}>
        <InputGroup w={'30vw'} minWidth={'300px'}>
          <Input
            type="text"
            placeholder="Will the world end in 2025?"
            value={q}
            onChange={e => setQ(e.target.value)}
            borderRadius={1}
          />
          <Link href={`${APP_HOST}/predict?q=${window.encodeURIComponent(q)}`}>
            <IconButton
              borderRadius={1}
              colorScheme="blue"
              aria-label="Predict"
              icon={<SearchIcon />}
            />
          </Link>
        </InputGroup>
      </Stack>
      <Stack direction="row" spacing={4}>
        <Button href="" rightIcon={<ExternalLinkIcon />} variant="outline">
          <Link href="https://github.com/sshh12/llm_oracle" isExternal>
            How does this work?
          </Link>
        </Button>
        <Button rightIcon={<SettingsIcon />} colorScheme="teal" variant="solid">
          Settings
        </Button>
      </Stack>
    </VStack>
  );
}

export default Predict;
