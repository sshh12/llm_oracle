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
  useDisclosure,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalCloseButton,
  ModalBody,
  ModalFooter,
  FormControl,
  FormLabel,
  Slider,
  SliderTrack,
  SliderFilledTrack,
  SliderThumb,
} from '@chakra-ui/react';
import { SearchIcon, SettingsIcon, ExternalLinkIcon } from '@chakra-ui/icons';
import { useLocalStorage } from '../hooks';

function Predict() {
  const [apiKey, setAPIKey] = useLocalStorage('oracle:apikey', () => '');
  const [modelTemp, setModelTemp] = useLocalStorage(
    'oracle:modelTemp',
    () => 50
  );
  const [recentResults] = useLocalStorage('oracle:recent', () => []);
  const [q, setQ] = useState('');
  const qValid = q.trim().length > 5;
  const predictURL = `${APP_HOST}/predict?q=${window.encodeURIComponent(
    q
  )}&apikey=${apiKey}&temp=${modelTemp}`;
  const onPredict = () => {
    if (qValid) {
      window.location.href = predictURL;
    }
  };
  if (predictURL)
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
              onKeyUp={e => {
                if (e.key === 'Enter') {
                  onPredict();
                }
              }}
            />
            <IconButton
              onClick={() => onPredict()}
              borderRadius={1}
              colorScheme={qValid ? 'blue' : 'red'}
              aria-label="Predict"
              icon={<SearchIcon />}
            />
          </InputGroup>
        </Stack>
        <Stack direction="row" spacing={4}>
          <Button href="" rightIcon={<ExternalLinkIcon />} variant="outline">
            <Link href="https://github.com/sshh12/llm_oracle" isExternal>
              How does this work?
            </Link>
          </Button>
          <SettingsModalButton
            {...{ apiKey, setAPIKey, modelTemp, setModelTemp }}
          />
        </Stack>
        {recentResults && (
          <VStack>
            {recentResults
              .toReversed()
              .slice(0, 10)
              .map(v => (
                <Link href={`/results/${v.id}`}>
                  <Text fontSize={'1rem'}>
                    <i>{v.question}</i>
                  </Text>
                </Link>
              ))}
          </VStack>
        )}
      </VStack>
    );
}

function SettingsModalButton({ apiKey, setAPIKey, modelTemp, setModelTemp }) {
  const { isOpen, onOpen, onClose } = useDisclosure();

  return (
    <>
      <Button
        onClick={onOpen}
        rightIcon={<SettingsIcon />}
        colorScheme="teal"
        variant="solid"
      >
        Settings
      </Button>

      <Modal onClose={onClose} isOpen={isOpen} isCentered>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Settings</ModalHeader>
          <ModalCloseButton />
          <ModalBody pb={6}>
            <VStack spacing={6}>
              <FormControl>
                <FormLabel>OpenAI Key</FormLabel>
                <Input
                  placeholder="(blank for shared demo key)"
                  value={apiKey}
                  onChange={e => setAPIKey(e.target.value)}
                />
              </FormControl>
              <FormControl>
                <FormLabel>Model Temperature</FormLabel>
                <Slider
                  defaultValue={modelTemp}
                  onChange={v => setModelTemp(v)}
                >
                  <SliderTrack>
                    <SliderFilledTrack />
                  </SliderTrack>
                  <SliderThumb />
                </Slider>
              </FormControl>
            </VStack>
          </ModalBody>
          <ModalFooter>
            <Button onClick={onClose}>Close & Save</Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
}

export default Predict;
