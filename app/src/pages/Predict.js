import React, { useState, useEffect } from 'react';
import { APP_HOST } from '../api';
import {
  Text,
  Link,
  VStack,
  Stack,
  Flex,
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
  Checkbox,
} from '@chakra-ui/react';
import { SearchIcon, SettingsIcon, ExternalLinkIcon } from '@chakra-ui/icons';
import { useLocalStorage } from '../hooks';

const PREDICTION_PLACEHOLDERS = [
  'Will the world end by 2050?',
  'Will next year be the hottest year on record?',
  'Will we discover extraterrestrial life within the next decade?',
  'Will there be a major technological breakthrough in the next 5 years?',
  'Will a universal basic income be implemented worldwide by 2040?',
  'Will AI surpass human intelligence by 2030?',
  'Will humans colonize Mars by 2050?',
  'Will there be a cure for cancer within the next 20 years?',
  'Will teleportation become a reality by 2100?',
  'Will climate change be reversed within the next 50 years?',
  'Will we achieve world peace by 2060?',
  'Will the global population reach 10 billion by 2050?',
  'Will we successfully reverse aging within the next 30 years?',
  'Will virtual reality become indistinguishable from reality by 2045?',
  'Will the majority of vehicles be self-driving by 2035?',
];

function Predict({ userId, user }) {
  const [placeholderIdx, setPlaceholderIdx] = useState(
    Math.floor(Math.random() * PREDICTION_PLACEHOLDERS.length)
  );
  const placeholderPrediction = PREDICTION_PLACEHOLDERS[placeholderIdx];
  const [apiKey, setAPIKey] = useLocalStorage('oracle:apikey', () => '');
  const [publicVisable, setPublicVisable] = useLocalStorage(
    'oracle:public',
    () => true
  );
  const [modelTemp, setModelTemp] = useLocalStorage(
    'oracle:modelTemp',
    () => 50
  );
  const [recentResults, setRecentResults] = useLocalStorage(
    'oracle:recent',
    () => []
  );
  const [q, setQ] = useState('');
  const predictURL = `${APP_HOST}/predict?q=${window.encodeURIComponent(
    q || placeholderPrediction
  )}&apikey=${apiKey}&temp=${modelTemp}&public=${publicVisable}&userId=${userId}`;
  const onPredict = () => {
    window.location.href = predictURL;
  };
  useEffect(() => {
    const timeout = setTimeout(() => {
      setPlaceholderIdx((placeholderIdx + 1) % PREDICTION_PLACEHOLDERS.length);
    }, 5000);

    return () => {
      clearTimeout(timeout);
    };
  }, [placeholderIdx]);
  if (predictURL)
    return (
      <VStack spacing={7}>
        <Text fontSize={'5rem'}>🔮</Text>
        <Stack spacing={1}>
          <InputGroup w={'40vw'} minWidth={'340px'}>
            <Input
              type="text"
              placeholder={placeholderPrediction}
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
              colorScheme={'blue'}
              aria-label="Predict"
              icon={<SearchIcon />}
            />
          </InputGroup>
        </Stack>
        <Flex wrap="wrap" justify="center">
          <Button m={2} rightIcon={<ExternalLinkIcon />} variant="outline">
            <Link href="https://github.com/sshh12/llm_oracle" isExternal>
              How does this work?
            </Link>
          </Button>
          <Button m={2} rightIcon={<ExternalLinkIcon />} variant="outline">
            <Link
              href={`${APP_HOST}/buy_predictions?userId=${userId}`}
              isExternal
            >
              Get predictions ({user?.predictions_remaining})
            </Link>
          </Button>
          <SettingsModalButton
            {...{
              apiKey,
              setAPIKey,
              modelTemp,
              setModelTemp,
              publicVisable,
              setPublicVisable,
              setRecentResults,
              userId,
            }}
          />
        </Flex>
        {recentResults && (
          <VStack>
            {recentResults.toReversed().map(v => (
              <Link key={v.id} href={`/results/${v.id}`}>
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

function SettingsModalButton({
  apiKey,
  setAPIKey,
  modelTemp,
  setModelTemp,
  publicVisable,
  setPublicVisable,
  setRecentResults,
  userId,
}) {
  const { isOpen, onOpen, onClose } = useDisclosure();

  return (
    <>
      <Button
        m={2}
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
                <FormLabel>User ID</FormLabel>
                <Text pb={'4px'}>
                  Purchased credits are tied to your user ID.
                </Text>
                <Input value={userId} disabled={true} />
              </FormControl>
              <FormControl>
                <FormLabel>OpenAI Key (Requires GPT-4)</FormLabel>
                <Input
                  placeholder="(blank for limited shared demo key)"
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
              <FormControl>
                <FormLabel>Public Predictions</FormLabel>
                <Checkbox
                  isChecked={publicVisable}
                  onChange={e => setPublicVisable(e.target.checked)}
                >
                  Viewable By Public
                </Checkbox>
              </FormControl>
              <FormControl>
                <FormLabel>Prediction History</FormLabel>
                <Text pb={'4px'}>
                  This does not delete predictions from the server, UI only.
                </Text>
                <Button colorScheme="red" onClick={() => setRecentResults([])}>
                  Clear History
                </Button>
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
